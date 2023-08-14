import os
import sys
import webbrowser
import subprocess
from glob import glob
from itertools import chain, combinations
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from ui_form import Ui_UmodelBruteForcer

class UmodelBruteForcer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_UmodelBruteForcer()
        self.ui.setupUi(self)

        # Connect the button for browsing .exe file
        self.ui.umodelExePushButton.clicked.connect(lambda: self.browse_file('exe', self.ui.umodelExeLineEdit))

        # Define folder buttons and their descriptions
        folder_buttons = {
            'gamePushButton': ("game's installation folder", self.ui.gameLineEdit),
            'gameCookedPushButton': ("game's Cooked folder", self.ui.gameCookedLineEdit),
            'gameAnimPushButton': ("game's Animations folder", self.ui.gameAnimLineEdit),
            'gameSoundPushButton': ("game's Sounds folder", self.ui.gameSoundLineEdit),
            'gameSmeshPushButton': ("game's StaticMeshes folder", self.ui.gameSmeshLineEdit),
            'gameTexPushButton': ("game's Textures folder", self.ui.gameTexLineEdit),
            'gameAdd1PushButton': ("first additional folder", self.ui.gameAdd1LineEdit),
            'gameAdd2PushButton': ("second additional folder", self.ui.gameAdd2LineEdit),
            'gameAdd3PushButton': ("third additional folder", self.ui.gameAdd3LineEdit),
            'destFolderPushButton': ("Destination folder", self.ui.destFolderLineEdit)
        }

        # Connect folder buttons
        for button_name, (description, line_edit) in folder_buttons.items():
            button = getattr(self.ui, button_name)
            button.clicked.connect(lambda desc=description, le=line_edit: self.browse_folder(desc, le))

        # Connect to executing the command
        self.ui.ProcessButton.clicked.connect(self.execute_command)

        # Connect to open URL
        self.ui.JMDigitalLogo.clicked.connect(lambda: webbrowser.open('https://jmd.vc'))
        
        # Connect the "Select All" checkboxes
        self.ui.gamesTabUe1CheckBoxSelectAll.toggled.connect(lambda state: self.select_all_checkboxes('gamesTabUe1CheckBoxSelectAll', state))
        self.ui.gamesTabUe2CheckBoxSelectAll.toggled.connect(lambda state: self.select_all_checkboxes('gamesTabUe2CheckBoxSelectAll', state))
        self.ui.gamesTabUe3CheckBoxSelectAll.toggled.connect(lambda state: self.select_all_checkboxes('gamesTabUe3CheckBoxSelectAll', state))
        self.ui.gamesTabUe4CheckBoxSelectAll.toggled.connect(lambda state: self.select_all_checkboxes('gamesTabUe4CheckBoxSelectAll', state))
        self.ui.optionsSelectAllCheckBox.toggled.connect(self.select_all_options_checkboxes)

        # Define game switches for each engine version (checkboxes and switches combined)
        self.game_switches = {
            'gamesTabUe1CheckBoxSelectAll': [
                'gamesTabUe1CheckBoxUe1',
                'gamesTabUe1CheckBoxUndying',
            ],
            'gamesTabUe2CheckBoxSelectAll': [
                'gamesTabUe2CheckBoxUt2',
                'gamesTabUe2CheckBoxUe2',
                'gamesTabUe2CheckBoxUc1',
                'gamesTabUe2CheckBoxScell',
                'gamesTabUe2CheckBoxScconv',
                'gamesTabUe2CheckBoxL2',
                'gamesTabUe2CheckBoxLoco',
                'gamesTabUe2CheckBoxBterr',
                'gamesTabUe2CheckBoxSwrc',
                'gamesTabUe2CheckBoxXiii',
                'gamesTabUe2CheckBoxT3',
                'gamesTabUe2CheckBoxSwat4',
                'gamesTabUe2CheckBoxBio',
                'gamesTabUe2CheckBoxRag2',
                'gamesTabUe2CheckBoxExt1',
                'gamesTabUe2CheckBoxAa2',
                'gamesTabUe2CheckBoxVang',
                'gamesTabUe2CheckBoxEos',
            ],
            'gamesTabUe3CheckBoxSelectAll': [
                'gamesTabUe3CheckBoxMass2',
                'gamesTabUe3CheckBoxTurok',
                'gamesTabUe3CheckBoxEndwar',
                'gamesTabUe3CheckBoxMass3',
                'gamesTabUe3CheckBoxR6v2',
                'gamesTabUe3CheckBoxMki',
                'gamesTabUe3CheckBoxTna',
                'gamesTabUe3CheckBoxBs',
                'gamesTabUe3CheckBoxMk',
                'gamesTabUe3CheckBoxGowj',
                'gamesTabUe3CheckBoxA51',
                'gamesTabUe3CheckBoxMkvdc',
                'gamesTabUe3CheckBoxMassl',
                'gamesTabUe3CheckBoxMass',
                'gamesTabUe3CheckBoxMkx',
                'gamesTabUe3CheckBoxFury',
                'gamesTabUe3CheckBoxGowu',
                'gamesTabUe3CheckBoxUe3',
                'gamesTabUe3CheckBoxTnaw',
                'gamesTabUe3CheckBoxBatman3',
                'gamesTabUe3CheckBoxMedge',
                'gamesTabUe3CheckBoxAo2',
                'gamesTabUe3CheckBoxMcarta',
                'gamesTabUe3CheckBoxXmen',
                'gamesTabUe3CheckBoxHuxley',
                'gamesTabUe3CheckBoxDoh',
                'gamesTabUe3CheckBoxStrang',
                'gamesTabUe3CheckBoxBatman',
                'gamesTabUe3CheckBoxTlr',
                'gamesTabUe3CheckBoxBatman2',
                'gamesTabUe3CheckBoxSf2',
                'gamesTabUe3CheckBoxDnd',
                'gamesTabUe3CheckBoxArgo',
                'gamesTabUe3CheckBoxShad',
                'gamesTabUe3CheckBoxArgo2',
                'gamesTabUe3CheckBoxHunt',
                'gamesTabUe3CheckBoxGunsl',
                'gamesTabUe3CheckBoxBorder',
                'gamesTabUe3CheckBoxCrime',
                'gamesTabUe3CheckBoxFrontl',
                'gamesTabUe3CheckBoxAva',
                'gamesTabUe3CheckBoxFronth',
                'gamesTabUe3CheckBoxBatman4',
                'gamesTabUe3CheckBox50cent',
                'gamesTabUe3CheckBoxTera',
                'gamesTabUe3CheckBoxApb',
                'gamesTabUe3CheckBoxMo',
                'gamesTabUe3CheckBoxMoh2010',
                'gamesTabUe3CheckBoxEns',
                'gamesTabUe3CheckBoxTrans1',
                'gamesTabUe3CheckBoxAcm',
                'gamesTabUe3CheckBoxTrans2',
                'gamesTabUe3CheckBoxSing',
                'gamesTabUe3CheckBoxBorder3',
                'gamesTabUe3CheckBoxLeg',
                'gamesTabUe3CheckBoxAa3',
                'gamesTabUe3CheckBoxBns',
                'gamesTabUe3CheckBoxAlpha',
                'gamesTabUe3CheckBoxMoha',
                'gamesTabUe3CheckBoxUndertow',
                'gamesTabUe3CheckBoxTrans',
                'gamesTabUe3CheckBoxBerk',
                'gamesTabUe3CheckBoxTrans3',
                'gamesTabUe3CheckBoxDarkv',
                'gamesTabUe3CheckBoxAlice',
                'gamesTabUe3CheckBoxPla',
                'gamesTabUe3CheckBoxXcom',
                'gamesTabUe3CheckBoxXcom2',
                'gamesTabUe3CheckBoxDis',
                'gamesTabUe3CheckBoxFablej',
                'gamesTabUe3CheckBoxRem',
                'gamesTabUe3CheckBoxLp3',
                'gamesTabUe3CheckBoxLp3y',
                'gamesTabUe3CheckBoxBio3',
                'gamesTabUe3CheckBoxT4',
                'gamesTabUe3CheckBoxTaoyuan',
                'gamesTabUe3CheckBoxFable',
                'gamesTabUe3CheckBoxBorder2',
                'gamesTabUe3CheckBoxRem2',
                'gamesTabUe3CheckBoxThief4',
                'gamesTabUe3CheckBoxDmc',
                'gamesTabUe3CheckBoxGigantic',
                'gamesTabUe3CheckBoxMurd',
                'gamesTabUe3CheckBoxSmite',
                'gamesTabUe3CheckBoxDundef',
                'gamesTabUe3CheckBoxSov',
                'gamesTabUe3CheckBoxMetroconf',
                'gamesTabUe3CheckBoxRocketleague',
                'gamesTabUe3CheckBoxDev3rd',
                'gamesTabUe3CheckBoxGuilty',
                'gamesTabUe3CheckBoxVec',
                'gamesTabUe3CheckBoxGrav',
                'gamesTabUe3CheckBoxDust514',
            ],
            'gamesTabUe4CheckBoxSelectAll': [
                'gamesTabUe4CheckBoxUe4p',
                'gamesTabUe4CheckBoxGears4',
                'gamesTabUe4CheckBoxDaysgone',
                'gamesTabUe4CheckBoxArk',
                'gamesTabUe4CheckBoxTekken7',
                'gamesTabUe4CheckBoxLawbr',
                'gamesTabUe4CheckBoxSod2',
                'gamesTabUe4CheckBoxDauntless',
                'gamesTabUe4CheckBoxParagon',
                'gamesTabUe4CheckBoxUt4',
                'gamesTabUe4CheckBoxHit',
                'gamesTabUe4CheckBoxNgb',
                'gamesTabUe4CheckBoxLis2',
                'gamesTabUe4CheckBoxAscl',
                'gamesTabUe4CheckBoxBorder3',
                'gamesTabUe4CheckBoxKh3',
                'gamesTabUe4CheckBoxJedi',
                'gamesTabUe4CheckBoxFablel',
                'gamesTabUe4CheckBoxSot',
            ],
        }
        
    def select_all_options_checkboxes(self, state):
        # Define the names of the checkboxes to be affected by the "Select All" option
        options_checkboxes = [
            'optionsNoMeCheckBox', 'optionsNoAnCheckBox', 'optionsNoStMeCheckBox',
            'optionsNoVeMeCheckBox', 'optionsNoTxCheckBox', 'optionsNoMpCheckBox',
            'optionsNoLiCheckBox', 'optionsZlibCheckBox', 'optionsLzxCheckBox', 'optionsLzoCheckBox'
        ]
    
        # Check or uncheck the checkboxes based on the state of the "Select All" checkbox
        for checkbox_name in options_checkboxes:
            checkbox_object = getattr(self.ui, checkbox_name)
            checkbox_object.setChecked(state)

    def select_all_checkboxes(self, select_all_key, state):
        # Retrieve the relevant checkboxes
        checkboxes = self.game_switches.get(select_all_key, [])
    
        # Check or uncheck the checkboxes based on the state of the "Select All" checkbox
        for checkbox_name in checkboxes:
            checkbox_object = getattr(self.ui, checkbox_name)
            checkbox_object.setChecked(state)

    def browse_file(self, file_type, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File', filter=f"{file_type} files (*.{file_type})")
        line_edit.setText(file_path)

    def browse_folder(self, description, line_edit):
        folder_path = QFileDialog.getExistingDirectory(self, f'Select Folder for {description}')
        line_edit.setText(folder_path)

    def build_command(self, game_switch, file_to_process, folder_name, dest_folder):
        # Get the path to umodel.exe
        umodel_exe_path = self.ui.umodelExeLineEdit.text()
        game_path = self.ui.gameLineEdit.text() # Retrieve from gameLineEdit

        # Usage: umodel [command] [options] <package> [<object> [<class>]]
        #        umodel [command] [options] <directory>
        #        umodel @<response_file>
        # 
        #     <package>       name of package to load - this could be a file name
        #                     with or without extension, or wildcard
        #     <object>        name of object to load
        #     <class>         class of object to load (useful, when trying to load
        #                     object with ambiguous name)
        #     <directory>     path to the game (see -path option)
        # 
        # Commands:
        #     -view           (default) visualize object; when no <object> specified
        #                     will load whole package
        #     -list           list contents of package
        #     -export         export specified object or whole package
        #     -save           save specified packages
        # 
        # Help information:
        #     -help           display this help page
        #     -version        display umodel version information
        #     -taglist        list of tags to override game autodetection (for -game=nnn option)
        #     -gamelist       list of supported games
        # 
        # Developer commands:
        #     -log=file       write log to the specified file
        #     -dump           dump object information to console
        #     -pkginfo        load package and display its information
        #     -testexport     perform fake export
        # 
        # Options:
        #     -path=PATH      path to game installation directory; if not specified,
        #                     program will search for packages in current directory
        #     -game=tag       override game autodetection (see -taglist for variants)
        #     -pkgver=nnn     override package version (advanced option!)
        #     -pkg=package    load extra package (in addition to <package>)
        #     -obj=object     specify object(s) to load
        #     -gui            force startup UI to appear
        #     -aes=key        provide AES decryption key for encrypted pak files,
        #                     key is ASCII or hex string (hex format is 0xAABBCCDD),
        #                     multiple options could be provided for multi-key games
        #     -aes=@file.txt  read AES decryption key(s) from a text file
        # 
        # Compatibility options:
        #     -nomesh         disable loading of SkeletalMesh classes in a case of
        #                     unsupported data format
        #     -noanim         disable loading of MeshAnimation classes
        #     -nostat         disable loading of StaticMesh class
        #     -novert         disable loading of VertMesh class
        #     -notex          disable loading of Material classes
        #     -nomorph        disable loading of MorphTarget class
        #     -nolightmap     disable loading of Lightmap textures
        #     -sounds         allow export of sounds
        #     -3rdparty       allow 3rd party asset export (ScaleForm, FaceFX)
        #     -lzo|lzx|zlib   force compression method for UE3 fully-compressed packages
        # 
        # Platform selection:
        #     -ps3            Playstation 3
        #     -ps4            Playstation 4
        #     -nsw            Nintendo Switch
        #     -ios            iOS (iPhone/iPad)
        #     -android        Android
        # 
        # Viewer options:
        #     -meshes         view meshes only
        #     -materials      view materials only (excluding textures)
        #     -anim=<set>     specify AnimSet to automatically attach to mesh
        # 
        # Export options:
        #     -out=PATH       export everything into PATH instead of the current directory
        #     -all            used with -dump, will dump all objects instead of specified one
        #     -uncook         use original package name as a base export directory (UE3)
        #     -groups         use group names instead of class names for directories (UE1-3)
        #     -uc             create unreal script when possible
        #     -psk            use ActorX format for meshes (default)
        #     -md5            use md5mesh/md5anim format for skeletal mesh
        #     -gltf           use glTF 2.0 format for mesh
        #     -lods           export all available mesh LOD levels
        #     -dds            export textures in DDS format whenever possible
        #     -png            export textures in PNG format instead of TGA
        #     -notgacomp      disable TGA compression
        #     -nooverwrite    prevent existing files from being overwritten (better
        #                     performance)
        # 
        # Supported resources for export:
        #     SkeletalMesh    exported as ActorX psk file, MD5Mesh or glTF
        #     MeshAnimation   exported as ActorX psa file or MD5Anim
        #     VertMesh        exported as Unreal 3d file
        #     StaticMesh      exported as psk file with no skeleton (pskx) or glTF
        #     Texture         exported in tga or dds format
        #     Sounds          file extension depends on object contents
        #     ScaleForm       gfx
        #     FaceFX          fxa
        #     Sound           exported "as is"

        # Define master switches
        master_switches = [
            '-nooverwrite' if self.ui.optionsNoOvCheckBox.isChecked() else '',
            '-sounds' if self.ui.optionsSndsCheckBox.isChecked() else '',
            '-3rdparty' if self.ui.options3rdPartyCheckBox.isChecked() else '',
            '-uc' if self.ui.optionsUScriptCheckBox.isChecked() else '',
            '-gltf' if self.ui.optionsGltfCheckBox.isChecked() else '',
            '-png' if self.ui.optionsPngCheckBox.isChecked() else '',
            '-groups' if self.ui.optionsGrpsCheckBox.isChecked() else '',
            '-lods' if self.ui.optionsLodsCheckBox.isChecked() else '',
            '-dds' if self.ui.optionsDdsCheckBox.isChecked() else '',
            '-ps3' if self.ui.optionsPs3CheckBox.isChecked() else '',
            '-ps4' if self.ui.optionsPs4CheckBox.isChecked() else '',
            '-nsw' if self.ui.optionsNswCheckBox.isChecked() else '',
            '-ios' if self.ui.optionsIosCheckBox.isChecked() else '',
            '-android' if self.ui.optionsAndroidCheckBox.isChecked() else '',
            '-notgacomp' if self.ui.optionsDisTgaCompCheckBox.isChecked() else '',
            '-md5' if self.ui.optionsMd5CheckBox.isChecked() else '',
            '-uncook' if self.ui.optionsUnckCheckBox.isChecked() else ''
        ]
    
        # Define combinable switches
        combinable_switches = [
            '-nomesh' if self.ui.optionsNoMeCheckBox.isChecked() else '',
            '-noanim' if self.ui.optionsNoAnCheckBox.isChecked() else '',
            '-nostat' if self.ui.optionsNoStMeCheckBox.isChecked() else '',
            '-novert' if self.ui.optionsNoVeMeCheckBox.isChecked() else '',
            '-notex' if self.ui.optionsNoTxCheckBox.isChecked() else '',
            '-nomorph' if self.ui.optionsNoMpCheckBox.isChecked() else '',
            '-nolightmap' if self.ui.optionsNoLiCheckBox.isChecked() else ''
        ]
    
        # Define exclusive switches
        exclusive_switches = [
            '-zlib' if self.ui.optionsZlibCheckBox.isChecked() else '',
            '-lzx' if self.ui.optionsLzxCheckBox.isChecked() else '',
            '-lzo' if self.ui.optionsLzoCheckBox.isChecked() else ''
        ]
    
        # Filter out empty strings
        master_switches = [switch for switch in master_switches if switch]
        combinable_switches = [switch for switch in combinable_switches if switch]
        exclusive_switches = [switch for switch in exclusive_switches if switch]
    
        # Create a set to store unique commands
        unique_commands = set()
    
        # Generate all combinations of selected combinable switches
        all_combinations = chain.from_iterable(combinations(combinable_switches, r) for r in range(len(combinable_switches) + 1))
    
        # Extract the last part of the folder name
        folder_name_last_part = os.path.basename(folder_name)
    
        # Create commands for each combination
        for combination in all_combinations:
            # Skip the combination where all combinable switches are used together
            if len(combination) == len(combinable_switches):
                continue

            for exclusive_switch in exclusive_switches + [None]:  # Include None to allow no exclusive switch
                umodel_options = " ".join(master_switches + list(combination))
                if exclusive_switch:
                    umodel_options += f" {exclusive_switch}"
    
                # Construct the command string
                command = f'"{umodel_exe_path}" -export {umodel_options} {game_switch} -path="{game_path}" "{file_to_process}" -out="{dest_folder}/{folder_name_last_part}"'
    
                # Add the command to the set of unique commands
                unique_commands.add(command)
    
        # Convert the set of unique commands to a list and sort by length from longest to shortest
        sorted_commands = sorted(unique_commands, key=lambda x: -len(x))
    
        return sorted_commands

    def execute_command(self):
        log_file_path = os.path.join(os.path.dirname(__file__), 'commands.bat')
        
        # Define game switches
        game_switches = {
            #UE1
            'gamesTabUe1CheckBoxUe1': '-game=ue1',
            'gamesTabUe1CheckBoxUndying': '-game=undying',

            #UE2
            'gamesTabUe2CheckBoxUt2': '-game=ut2',
            'gamesTabUe2CheckBoxUe2': '-game=ue2',
            'gamesTabUe2CheckBoxUc1': '-game=uc1',
            'gamesTabUe2CheckBoxScell': '-game=scell',
            'gamesTabUe2CheckBoxScconv': '-game=scconv',
            'gamesTabUe2CheckBoxL2': '-game=l2',
            'gamesTabUe2CheckBoxLoco': '-game=loco',
            'gamesTabUe2CheckBoxBterr': '-game=bterr',
            'gamesTabUe2CheckBoxSwrc': '-game=swrc',
            'gamesTabUe2CheckBoxXiii': '-game=xiii',
            'gamesTabUe2CheckBoxT3': '-game=t3',
            'gamesTabUe2CheckBoxSwat4': '-game=swat4',
            'gamesTabUe2CheckBoxBio': '-game=bio',
            'gamesTabUe2CheckBoxRag2': '-game=rag2',
            'gamesTabUe2CheckBoxExt1': '-game=extl',
            'gamesTabUe2CheckBoxAa2': '-game=aa2',
            'gamesTabUe2CheckBoxVang': '-game=vang',
            'gamesTabUe2CheckBoxEos': '-game=eos',

            #UE3
            'gamesTabUe3CheckBoxMass2': '-game=mass2',
            'gamesTabUe3CheckBoxTurok': '-game=turok',
            'gamesTabUe3CheckBoxEndwar': '-game=endwar',
            'gamesTabUe3CheckBoxMass3': '-game=mass3',
            'gamesTabUe3CheckBoxR6v2': '-game=r6v2',
            'gamesTabUe3CheckBoxMki': '-game=mk',
            'gamesTabUe3CheckBoxTna': '-game=tna',
            'gamesTabUe3CheckBoxBs': '-game=bs',
            'gamesTabUe3CheckBoxMk': '-game=mk',
            'gamesTabUe3CheckBoxGowj': '-game=gowj',
            'gamesTabUe3CheckBoxA51': '-game=a51',
            'gamesTabUe3CheckBoxMkvdc': '-game=mk',
            'gamesTabUe3CheckBoxMassl': '-game=massl',
            'gamesTabUe3CheckBoxMass': '-game=mass',
            'gamesTabUe3CheckBoxMkx': '-game=mk',
            'gamesTabUe3CheckBoxFury': '-game=fury',
            'gamesTabUe3CheckBoxGowu': '-game=gowu',
            'gamesTabUe3CheckBoxUe3': '-game=ue3',
            'gamesTabUe3CheckBoxTnaw': '-game=tna',
            'gamesTabUe3CheckBoxBatman3': '-game=batman3',
            'gamesTabUe3CheckBoxMedge': '-game=medge',
            'gamesTabUe3CheckBoxAo2': '-game=ao2',
            'gamesTabUe3CheckBoxMcarta': '-game=mcarta',
            'gamesTabUe3CheckBoxXmen': '-game=xmen',
            'gamesTabUe3CheckBoxHuxley': '-game=huxley',
            'gamesTabUe3CheckBoxDoh': '-game=doh',
            'gamesTabUe3CheckBoxStrang': '-game=strang',
            'gamesTabUe3CheckBoxBatman': '-game=batman',
            'gamesTabUe3CheckBoxTlr': '-game=tlr',
            'gamesTabUe3CheckBoxBatman2': '-game=batman2',
            'gamesTabUe3CheckBoxSf2': '-game=sf2',
            'gamesTabUe3CheckBoxDnd': '-game=dnd',
            'gamesTabUe3CheckBoxArgo': '-game=argo',
            'gamesTabUe3CheckBoxShad': '-game=shad',
            'gamesTabUe3CheckBoxArgo2': '-game=argo',
            'gamesTabUe3CheckBoxHunt': '-game=hunt',
            'gamesTabUe3CheckBoxGunsl': '-game=gunsl',
            'gamesTabUe3CheckBoxBorder': '-game=border',
            'gamesTabUe3CheckBoxCrime': '-game=crime',
            'gamesTabUe3CheckBoxFrontl': '-game=frontl',
            'gamesTabUe3CheckBoxAva': '-game=ava',
            'gamesTabUe3CheckBoxFronth': '-game=frontl',
            'gamesTabUe3CheckBoxBatman4': '-game=batman4',
            'gamesTabUe3CheckBox50cent': '-game=50cent',
            'gamesTabUe3CheckBoxTera': '-game=tera',
            'gamesTabUe3CheckBoxApb': '-game=apb',
            'gamesTabUe3CheckBoxMo': '-game=mo',
            'gamesTabUe3CheckBoxMoh2010': '-game=moh2010',
            'gamesTabUe3CheckBoxEns': '-game=ens',
            'gamesTabUe3CheckBoxTrans1': '-game=trans',
            'gamesTabUe3CheckBoxAcm': '-game=acm',
            'gamesTabUe3CheckBoxTrans2': '-game=trans',
            'gamesTabUe3CheckBoxSing': '-game=sing',
            'gamesTabUe3CheckBoxBorder3': '-game=border',
            'gamesTabUe3CheckBoxLeg': '-game=leg',
            'gamesTabUe3CheckBoxAa3': '-game=aa3',
            'gamesTabUe3CheckBoxBns': '-game=bns',
            'gamesTabUe3CheckBoxAlpha': '-game=alpha',
            'gamesTabUe3CheckBoxMoha': '-game=moha',
            'gamesTabUe3CheckBoxUndertow': '-game=undertow',
            'gamesTabUe3CheckBoxTrans': '-game=trans',
            'gamesTabUe3CheckBoxBerk': '-game=berk',
            'gamesTabUe3CheckBoxTrans3': '-game=trans',
            'gamesTabUe3CheckBoxDarkv': '-game=darkv',
            'gamesTabUe3CheckBoxAlice': '-game=alice',
            'gamesTabUe3CheckBoxPla': '-game=pla',
            'gamesTabUe3CheckBoxXcom': '-game=xcom',
            'gamesTabUe3CheckBoxXcom2': '-game=xcom2',
            'gamesTabUe3CheckBoxDis': '-game=dis',
            'gamesTabUe3CheckBoxFablej': '-game=fable',
            'gamesTabUe3CheckBoxRem': '-game=rem',
            'gamesTabUe3CheckBoxLp3': '-game=lp3',
            'gamesTabUe3CheckBoxLp3y': '-game=lp3',
            'gamesTabUe3CheckBoxBio3': '-game=bio3',
            'gamesTabUe3CheckBoxT4': '-game=t4',
            'gamesTabUe3CheckBoxTaoyuan': '-game=taoyuan',
            'gamesTabUe3CheckBoxFable': '-game=fable',
            'gamesTabUe3CheckBoxBorder2': '-game=border',
            'gamesTabUe3CheckBoxRem2': '-game=rem',
            'gamesTabUe3CheckBoxThief4': '-game=thief4',
            'gamesTabUe3CheckBoxDmc': '-game=dmc',
            'gamesTabUe3CheckBoxGigantic': '-game=gigantic',
            'gamesTabUe3CheckBoxMurd': '-game=murd',
            'gamesTabUe3CheckBoxSmite': '-game=smite',
            'gamesTabUe3CheckBoxDundef': '-game=dundef',
            'gamesTabUe3CheckBoxSov': '-game=sov',
            'gamesTabUe3CheckBoxMetroconf': '-game=metroconf',
            'gamesTabUe3CheckBoxRocketleague': '-game=rocketleague',
            'gamesTabUe3CheckBoxDev3rd': '-game=dev3rd',
            'gamesTabUe3CheckBoxGuilty': '-game=guilty',
            'gamesTabUe3CheckBoxVec': '-game=vec',
            'gamesTabUe3CheckBoxGrav': '-game=grav',
            'gamesTabUe3CheckBoxDust514': '-game=dust514',
			
            #UE4
            'gamesTabUe4CheckBoxUe4p': '-game=ue4.25+',
            'gamesTabUe4CheckBoxGears4': '-game=gears4',
            'gamesTabUe4CheckBoxDaysgone': '-game=daysgone',
            'gamesTabUe4CheckBoxArk': '-game=ark',
            'gamesTabUe4CheckBoxTekken7': '-game=tekken7',
            'gamesTabUe4CheckBoxLawbr': '-game=lawbr',
            'gamesTabUe4CheckBoxSod2': '-game=sod2',
            'gamesTabUe4CheckBoxDauntless': '-game=dauntless',
            'gamesTabUe4CheckBoxParagon': '-game=paragon',
            'gamesTabUe4CheckBoxUt4': '-game=ut4',
            'gamesTabUe4CheckBoxHit': '-game=hit',
            'gamesTabUe4CheckBoxNgb': '-game=ngb',
            'gamesTabUe4CheckBoxLis2': '-game=lis2',
            'gamesTabUe4CheckBoxAscl': '-game=asc1',
            'gamesTabUe4CheckBoxBorder3': '-game=border3',
            'gamesTabUe4CheckBoxKh3': '-game=kh3',
            'gamesTabUe4CheckBoxJedi': '-game=jedi',
            'gamesTabUe4CheckBoxFablel': '-game=fablel',
            'gamesTabUe4CheckBoxSot': '-game=sot'
        }

        # Define default extensions
        default_extensions = {
            'gameCookedLineEdit': 'upk',
            'gameAnimLineEdit': 'ukx',
            'gameSmeshLineEdit': 'usx',
            'gameSoundLineEdit': 'uax',
            'gameTexLineEdit': 'utx',
        }
        
        # Define folder processing information
        folders_to_process = {
            self.ui.gameCookedLineEdit.text(): self.ui.gameCookedExtLineEdit.text() if self.ui.gameCookedExtLineEdit.text() else default_extensions['gameCookedLineEdit'],
            self.ui.gameAnimLineEdit.text(): self.ui.gameAnimExtLineEdit.text() if self.ui.gameAnimExtLineEdit.text() else default_extensions['gameAnimLineEdit'],
            self.ui.gameSmeshLineEdit.text(): self.ui.gameSmeshExtLineEdit.text() if self.ui.gameSmeshExtLineEdit.text() else default_extensions['gameSmeshLineEdit'],
            self.ui.gameSoundLineEdit.text(): self.ui.gameSoundExtLineEdit.text() if self.ui.gameSoundExtLineEdit.text() else default_extensions['gameSoundLineEdit'],
            self.ui.gameTexLineEdit.text(): self.ui.gameTexExtLineEdit.text() if self.ui.gameTexExtLineEdit.text() else default_extensions['gameTexLineEdit'],
            self.ui.gameAdd1LineEdit.text(): self.ui.gameAdd1ExtLineEdit.text(),
            self.ui.gameAdd2LineEdit.text(): self.ui.gameAdd2ExtLineEdit.text(),
            self.ui.gameAdd3LineEdit.text(): self.ui.gameAdd3ExtLineEdit.text(),
        }

        # Identify selected game switches and store them in a set (unique values only)
        selected_game_switches = set([switch for checkbox_name, switch in game_switches.items() if getattr(self.ui, checkbox_name).isChecked()])

        # Iterate through selected game switches
        for game_switch in selected_game_switches:
            # Open the log file in append mode
            with open(log_file_path, 'a') as log_file:
                # Destination folder
                dest_folder = self.ui.destFolderLineEdit.text()
                
                # Iterate through folders and process files
                for folder_path, extensions in folders_to_process.items():
                    # Skip if no folder or extension provided
                    if not folder_path or not extensions:
                        continue
    
                    # Get the folder name (e.g., "Animations", "Sounds")
                    folder_name = folder_path.split('\\')[-1]
    
                    # Process files with the specified extensions
                    for ext in extensions.split(','):
                        file_paths = glob(f"{folder_path}\\*.{ext.strip()}")
                        for file_path in file_paths:
                            commands = self.build_command(game_switch, file_path, folder_name, dest_folder)
                            for command in commands:
                                # Write the command to the log file
                                log_file.write(command + '\n')
                            
                                subprocess.run(command, shell=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = UmodelBruteForcer()
    widget.show()
    sys.exit(app.exec())
