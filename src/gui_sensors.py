from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                               QMessageBox, QInputDialog, QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

import api
import settings
import icons as icons

import logging_config  # Setup the logging  # noqa: F401
import logging

logger = logging.getLogger(__name__)


class SensorSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Entity")
        
        self.selected_entities = {}
        self.entity_types = {}
        
        # Get entities from API
        self.entities = api.list_states()
        self.entity_list = []
        
        if self.entities and isinstance(self.entities, list):
            for entity in self.entities:
                if isinstance(entity, dict) and "entity_id" in entity:
                    self.entity_list.append(entity["entity_id"])
        
        self.setup_ui()
        self.load_selected_entities()
        self.adjustSize()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Entity selection
        layout.addWidget(QLabel("Choose an entity:"))
        
        self.combobox = QComboBox()
        self.combobox.addItems(sorted(self.entity_list))
        self.combobox.setEditable(True)
        layout.addWidget(self.combobox)
        
        # Add button
        self.btn_add = QPushButton("Add Entity")
        self.btn_add.clicked.connect(self.on_add_entity)
        layout.addWidget(self.btn_add)
        
        # Table for selected entities
        self.selected_table = QTableWidget()
        self.selected_table.setColumnCount(3)
        self.selected_table.setHorizontalHeaderLabels(["Entity ID", "Friendly Name", "Type"])
        
        # Set column widths
        header = self.selected_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        self.selected_table.cellDoubleClicked.connect(self.on_table_double_click)
        layout.addWidget(self.selected_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.btn_save = QPushButton("Save Selection")
        self.btn_remove = QPushButton("Remove Selected")
        
        self.btn_save.clicked.connect(self.on_save_selection)
        self.btn_remove.clicked.connect(self.on_remove_selected)
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_remove)
        
        layout.addLayout(button_layout)
        
        # Set window icon after UI is set up
        self.setWindowIcon(icons.get_icon('database_24dp_1976d2_fill0_wght400_grad0_opsz24'))

    def on_add_entity(self):
        entity_id = self.combobox.currentText()
        if not entity_id:
            return
            
        # Find friendly name from entities
        friendly_name = entity_id
        for entity in self.entities:
            if entity["entity_id"] == entity_id:
                friendly_name = entity.get("attributes", {}).get("friendly_name", entity_id)
                break
        
        if entity_id and entity_id not in self.selected_entities:
            self.selected_entities[entity_id] = friendly_name
            
            # Add to table
            row = self.selected_table.rowCount()
            self.selected_table.insertRow(row)
            self.selected_table.setItem(row, 0, QTableWidgetItem(entity_id))
            self.selected_table.setItem(row, 1, QTableWidgetItem(friendly_name))
            self.selected_table.setItem(row, 2, QTableWidgetItem("sensor"))
            
            # Default type is 'sensor'
            self.entity_types[entity_id] = "sensor"

    def on_table_double_click(self, row, column):
        if column == 2:  # Type column
            entity_id = self.selected_table.item(row, 0).text()
            current_type = self.entity_types.get(entity_id, "sensor")
            
            types = ["sensor", "switch"]
            selected_type, ok = QInputDialog.getItem(
                self, "Entity Type", "Select type for entity:", 
                types, types.index(current_type), False
            )
            
            if ok:
                self.selected_table.setItem(row, 2, QTableWidgetItem(selected_type))
                self.entity_types[entity_id] = selected_type

    def on_save_selection(self):
        # Gather selected entities and types
        selected = []
        for row in range(self.selected_table.rowCount()):
            entity_id = self.selected_table.item(row, 0).text()
            friendly_name = self.selected_table.item(row, 1).text()
            entity_type = self.selected_table.item(row, 2).text()
            selected.append({
                "entity_id": entity_id, 
                "friendly_name": friendly_name, 
                "type": entity_type
            })
        
        # Save to settings
        settings.save_config("entities", selected)
        QMessageBox.information(self, "Saved", "Selection saved!")

    def on_remove_selected(self):
        current_row = self.selected_table.currentRow()
        if current_row >= 0:
            entity_id = self.selected_table.item(current_row, 0).text()
            self.selected_table.removeRow(current_row)
            self.entity_types.pop(entity_id, None)
            self.selected_entities.pop(entity_id, None)

    def load_selected_entities(self):
        # Load from settings
        selected = settings.load_value_from_json_file("entities")
        if not selected:
            return
            
        for item in selected:
            entity_id = item.get("entity_id", "")
            friendly_name = item.get("friendly_name", entity_id)
            entity_type = item.get("type", "sensor")
            
            row = self.selected_table.rowCount()
            self.selected_table.insertRow(row)
            self.selected_table.setItem(row, 0, QTableWidgetItem(entity_id))
            self.selected_table.setItem(row, 1, QTableWidgetItem(friendly_name))
            self.selected_table.setItem(row, 2, QTableWidgetItem(entity_type))
            
            self.entity_types[entity_id] = entity_type
            self.selected_entities[entity_id] = friendly_name