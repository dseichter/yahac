import wx

import api
import settings

entities = api.list_states()

# Create a list of entity IDs to select as sensors
entity_list = []
selected_entities = {}  # key: entity_id, value: friendly_name
for entity in entities:
    entity_list.append(entity["entity_id"])


class SensorSelectorFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Select Entity", size=(500, 220))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Set frame icon
        frame_icon = wx.Icon(wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_OTHER, (16, 16)))
        self.SetIcon(frame_icon)

        label = wx.StaticText(panel, label="Choose an entity:")
        vbox.Add(label, flag=wx.LEFT | wx.TOP, border=10)

        self.combobox = wx.ComboBox(panel, choices=entity_list, style=wx.CB_DROPDOWN | wx.CB_SORT)
        vbox.Add(self.combobox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Add button to select entity
        self.btn_add = wx.Button(panel, label="Add Entity")
        vbox.Add(self.btn_add, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.btn_add.Bind(wx.EVT_BUTTON, self.on_add_entity)

        # Table to show selected entities
        self.selected_table = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.selected_table.InsertColumn(0, "Entity ID", width=200)
        self.selected_table.InsertColumn(1, "Friendly Name", width=180)
        self.selected_table.InsertColumn(2, "Type", width=90)

        vbox.Add(self.selected_table, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)

        # Save button
        self.btn_save = wx.Button(panel, label="Save Selection")
        vbox.Add(self.btn_save, flag=wx.ALIGN_RIGHT | wx.ALL, border=10)
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save_selection)

        panel.SetSizer(vbox)

        # Enable typing/searching in the combobox
        self.combobox.Bind(wx.EVT_TEXT, self.on_search)

        # Store type selection for each entity
        self.entity_types = {}

        # Bind table click for type selection
        self.selected_table.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_table_select)

        # Load previously saved entities
        self.load_selected_entities()

    def on_search(self, event):
        # Optionally, implement live filtering here
        pass

    def on_add_entity(self, event):
        entity_id = self.combobox.GetValue()
        # Find friendly name from entities
        friendly_name = entity_id
        for entity in entities:
            if entity["entity_id"] == entity_id:
                friendly_name = entity.get("attributes", {}).get("friendly_name", entity_id)
                break
        if entity_id and entity_id not in selected_entities:
            selected_entities[entity_id] = friendly_name
            index = self.selected_table.InsertItem(self.selected_table.GetItemCount(), entity_id)
            self.selected_table.SetItem(index, 1, friendly_name)
            # Default type is 'sensor'
            self.selected_table.SetItem(index, 2, "sensor")
            self.entity_types[entity_id] = "sensor"

    def on_table_select(self, event):
        # Allow user to change type between 'sensor' and 'switch'
        index = event.GetIndex()
        entity_id = self.selected_table.GetItemText(index)
        current_type = self.entity_types.get(entity_id, "sensor")
        dlg = wx.SingleChoiceDialog(self, "Select type for entity:", "Entity Type", ["sensor", "switch"], wx.CHOICEDLG_STYLE)
        dlg.SetSelection(0 if current_type == "sensor" else 1)
        if dlg.ShowModal() == wx.ID_OK:
            selected_type = dlg.GetStringSelection()
            self.selected_table.SetItem(index, 2, selected_type)
            self.entity_types[entity_id] = selected_type
        dlg.Destroy()

    def on_save_selection(self, event):
        # Gather selected entities and types
        selected = []
        for idx in range(self.selected_table.GetItemCount()):
            entity_id = self.selected_table.GetItemText(idx)
            friendly_name = self.selected_table.GetItem(idx, 1).GetText()
            entity_type = self.selected_table.GetItem(idx, 2).GetText()
            selected.append({"entity_id": entity_id, "friendly_name": friendly_name, "type": entity_type})
        # Save to settings
        settings.save_config("entities", selected)
        wx.MessageBox("Selection saved!", "Saved", wx.OK | wx.ICON_INFORMATION)

    def load_selected_entities(self):
        # Load from settings
        selected = settings.load_value_from_json_file("entities")
        if not selected:
            return
        for item in selected:
            entity_id = item.get("entity_id", "")
            friendly_name = item.get("friendly_name", entity_id)
            entity_type = item.get("type", "sensor")
            index = self.selected_table.InsertItem(self.selected_table.GetItemCount(), entity_id)
            self.selected_table.SetItem(index, 1, friendly_name)
            self.selected_table.SetItem(index, 2, entity_type)
            self.entity_types[entity_id] = entity_type
