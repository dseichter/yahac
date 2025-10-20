# Copyright (c) 2024 Daniel Seichter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import wx.tools.img2py as img2py
import os

from PIL import Image

# Iterate through all the png files in the icons directory
# and generate the icon file
# The icon file is generated in the src directory to be used in the application
append = False
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.png'):
            # Generate the icon file
            img2py.img2py(os.path.join(root, file), '../src/icons.py', append=append, imgName=file[:-4].lower(), icon=True, catalog=True, compressed=True)
            append = True

# Open the PNG file and save as ICO
with Image.open("home_app_logo_24dp_1976D2_FILL0_wght400_GRAD0_opsz24.png") as img:
    # Save as ICO (you can specify multiple sizes)
    img.save("yahac.ico", format="ICO", sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])