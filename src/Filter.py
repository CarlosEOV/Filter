# pylint: disable=no-member
import PySimpleGUI as sg
import io
import os
from PIL import Image, ImageGrab
from PySimpleGUI.PySimpleGUI import main
from Decoder_IMG import *
from Filters import *

RESOLUTION = (ImageGrab.grab().size)
COL_SIZE = (int(RESOLUTION[0] / 2) - 25, RESOLUTION[1])
FRM_SIZE = (COL_SIZE[0] , int((COL_SIZE[1] / 3) * 2) )
IMG_SIZE = (COL_SIZE[0] , int((COL_SIZE[1] / 3) * 2) )
BG_COLOR = '#2f363d'
MAIN_COLOR = '#1a1d21'
SEC_COLOR = '#353942'
TXT_COLOR = '#d5d8e0'

sg.theme('DarkBlue2')

def start_filter_GUI():
    OG_IMG = None
    F_IMG = None

    menu_toolbar = [['&File', ['&Open', '&Save', '&Exit']],
                
                ['&Filters', ['&Grayscales' , ['Average Grayscale', 'Grayscale', 'Luma Grayscale', '---',  
                                                'Max and Min Grayscale', 'Max Grayscale', 'Min Grayscale', '---',  
                                                'Red Grayscale', 'Green Grayscale', 'Blue Grayscale', '---', 
                                                'Shades of Gray'],
                             '&Brightness', '&Mosaic', '&High contrast', '&Inverted', '&RGB components', 
                             '&Convolution', ['&Blur', '&Motion blur', '&Find edges' , '&Sharpen', '&Emboss'],
                             '&Text', ['&Color Ms', '&Grayscale Ms', '---', '&Color characters', '&Black and White characters', 
                             '&Grayscale characters', '---', '&Sign', '---', '&Black dominoes', '&White dominoes','---', '&Cards'],
                             ]],
                
                ['&Help', '&About...'], ]
    
    column1_layout = [
        [sg.Frame(title='Original image', layout=[[sg.Image(size=IMG_SIZE, pad=(0, 5), key='-OG_IMAGE-', background_color=BG_COLOR)]], background_color=BG_COLOR, size=FRM_SIZE, key='-OGF_IMAGE-', relief=sg.RELIEF_RAISED)]
        
    ]

    column2_layout = [
        [sg.Frame(title='Modified image', layout=[[sg.Image(size=IMG_SIZE, pad=(0, 5), key='-F_IMAGE-', background_color=BG_COLOR)]], background_color=BG_COLOR, size=FRM_SIZE, key='-FF_IMAGE-', relief=sg.RELIEF_RAISED)]
    ]

    main_layout = [
        [sg.Menu(menu_definition=menu_toolbar, tearoff=False, background_color=MAIN_COLOR, text_color=TXT_COLOR)],
        [sg.Column(column1_layout, size=COL_SIZE, background_color= MAIN_COLOR, ),
         sg.VerticalSeparator(), 
         sg.Column(column2_layout, size=COL_SIZE, background_color=MAIN_COLOR)
        ],
    ]
    
    main_window = sg.Window('Filter app',
                            layout=main_layout,
                            size=RESOLUTION,
                            resizable=True,                          
                            background_color=MAIN_COLOR,
    )

    while True:
        event, values = main_window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        # ------ Process menu choices ------ #
        if event == 'Open':
            filename = sg.popup_get_file('File to open', no_window=True, keep_on_top=True, modal=True, file_types=(("PNG, JPG", "*.png *.jpg"),))
            img, img_bytes = convert_to_bytes(filename)
            if img != None and img_bytes != None:
                pb_layout = [[sg.Text('Loading...')],
                             [sg.ProgressBar(max_value=10, orientation='h', size=(40, 15), key='-PGRB-')]
                            ]

                pb_window = sg.Window('Loading image', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                progress_bar.update_bar(2)
                OG_IMG = img.copy()
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(5)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                img.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-OG_IMAGE-'].update(data=get_bytes(img), size=IMG_SIZE)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()

        if F_IMG != None:
            if event == 'Save':
                filename = ask_for_filename(default_filename='My_filter_img.png')
                if filename != None:
                    F_IMG.save(filename, format='PNG')

        if OG_IMG != None:
            pb_layout = [[sg.Text('Loading...')],
                         [sg.ProgressBar(max_value=10, orientation='h', size=(45, 15), key='-PGRB-')]
                        ]
            if event == 'Average Grayscale':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)

            elif event == 'Grayscale':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)

            elif event == 'Luma Grayscale':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'Max and Min Grayscale':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG,  main_window)

            elif event == 'Max Grayscale':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'Min Grayscale':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)

            elif event == 'Red Grayscale':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'Green Grayscale':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)

            elif event == 'Blue Grayscale':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)

            elif event == 'Shades of Gray':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)

            elif event == 'Brightness':
                b_event, b_values = sg.Window('Brightness', [
                    [sg.T('Adjust brightness')],
                    [sg.Slider(range=(-180, 180), default_value=0, resolution=1, tick_interval=100, 
                                orientation='h', border_width=3, size=(40, 10), key='-BRGHT-', tooltip='Brightness')],
                    [sg.Button('Ok')]
                ], modal=True, keep_on_top=True).read(close=True)
                brightness_value = b_values['-BRGHT-']
                if brightness_value != None:
                    F_IMG = OG_IMG.copy()
                    apply_filter(event, F_IMG, main_window, int(brightness_value))                    

            elif event == 'Mosaic':
                b_event, b_values = sg.Window('Mosaic', [
                    [sg.T('Adjust mosaic size')],
                    [sg.T('Height')],
                    [sg.Slider(range=(10, 100), default_value=10, resolution=1, tick_interval=20, 
                                orientation='h', border_width=3, size=(40, 10), key='-H_VALUE-', tooltip='Height')],
                    [sg.T('Width')],
                    [sg.Slider(range=(10, 100), default_value=10, resolution=1, tick_interval=20, 
                                orientation='h', border_width=3, size=(40, 10), key='-W_VALUE-', tooltip='Width')],
                    [sg.Button('Ok')]
                ], modal=True, keep_on_top=True).read(close=True)
                w_value = b_values['-W_VALUE-']
                h_value = b_values['-H_VALUE-']

                if w_value != None and h_value != None:
                    F_IMG = OG_IMG.copy()
                    apply_filter(event, F_IMG, main_window, int(w_value), int(h_value))
                    
            elif event == 'High contrast':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'Inverted':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)

            elif event == 'RGB components':
                b_event, b_values = sg.Window('RGB components', [
                    [sg.T('Adjust RGB components')],
                    [sg.T('Red')],
                    [sg.Slider(range=(0, 255), default_value=0, resolution=1, tick_interval=40, 
                                orientation='h', border_width=3, size=(40, 10), key='-R_VALUE-', tooltip='Red')],
                    [sg.T('Green')],
                    [sg.Slider(range=(0, 255), default_value=0, resolution=1, tick_interval=40, 
                                orientation='h', border_width=3, size=(40, 10), key='-G_VALUE-', tooltip='Green')],
                    [sg.T('Blue')],
                    [sg.Slider(range=(0, 255), default_value=0, resolution=1, tick_interval=40, 
                                orientation='h', border_width=3, size=(40, 10), key='-B_VALUE-', tooltip='Blue')],
                    [sg.Button('Ok')]
                ], modal=True, keep_on_top=True).read(close=True)
                
                red = b_values['-R_VALUE-']
                green = b_values['-G_VALUE-']
                blue = b_values['-B_VALUE-']
                
                if red != None and green != None and blue != None:
                    F_IMG = OG_IMG.copy()
                    apply_filter(event, F_IMG, main_window, int(red), int(green), int(blue))
                    
            elif event == 'Blur':
                b_event, b_values = sg.Window('Blur', [
                    [sg.T('Select intensity matrix for blur filter')],
                    [sg.Radio(text='3x3 Matrix', group_id=1, default=True, key='-3_M-'), 
                     sg.Radio(text='5x5 Matrix', group_id=1, default=False, key='-5_M-')
                    ],
                    [sg.Button('Ok')]
                ], modal=True, keep_on_top=True).read(close=True)

                selection = 0 if b_values['-3_M-'] else 1
                
                if selection != None:
                    F_IMG = OG_IMG.copy()
                    apply_filter(event, F_IMG, main_window, selection)
            
            elif event == 'Motion blur':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
                
            elif event == 'Find edges':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'Sharpen':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'Emboss':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)

            elif event == 'Color Ms':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'Grayscale Ms':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'Black and White characters':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'Color characters':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'Grayscale characters':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'Sign':
                s_event, s_values = sg.Window('Sign', layout=[
                    [sg.T('Type a message for sign filter (20 characters maximum)')],
                    [sg.Input(default_text='This is my message', size=(80, 10), tooltip='Type something!', do_not_clear=False, key='-SIGN_TXT-')],
                    [sg.Button('Ok')]
                ], modal=True, keep_on_top=True).read(close=True)

                message = s_values['-SIGN_TXT-']

                if message != None:
                    F_IMG = OG_IMG.copy()
                    apply_filter(event, F_IMG, main_window, message)
                
            elif event == 'Black dominoes':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'White dominoes':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)
            
            elif event == 'Cards':
                F_IMG = OG_IMG.copy()
                apply_filter(event, F_IMG, main_window)

        if event == 'About...':
            sg.popup('Filter App', 'Version 1.03', 'Carlos Eduardo Orozco Viveros', 'Release date: 05/31/21',
                     grab_anywhere=True, modal=True, 
                     background_color=MAIN_COLOR, text_color=TXT_COLOR, no_titlebar=True)

    main_window.close()

def ask_for_filename(default_filename='', initial_folder=None, size=None):
    
    if initial_folder is None:
        initial_folder = os.getcwd()

    save_layout = [[
                    sg.InputText(key='-FILETOSAVE-', default_text=default_filename, enable_events=True, justification='l'),
                    sg.InputText(key='-SAVEAS-', do_not_clear=False, enable_events=True, visible=False, ),
                    sg.FileSaveAs('Select', initial_folder=initial_folder, file_types=(("PNG", "*.png"),))],
                    [sg.Button('OK', bind_return_key=True), sg.Button('Cancel')]
    ]

    save_window = sg.Window('Save image', save_layout, keep_on_top=True,  modal=True)

    while True:
        event, values = save_window.Read()
        if event is None or event == 'Cancel':
            save_window.close()
            return None
        elif event == '-SAVEAS-':
            filename = values['-SAVEAS-']
            if filename:
                save_window['-FILETOSAVE-'].update(value=filename)
        elif event == "OK":
            save_window.close()
            return values['-FILETOSAVE-']

def apply_filter(filter_name, F_IMG, main_window, param_1=0, param_2=0, param_3=0):
    pb_layout = [[sg.Text('Loading...')],
                         [sg.ProgressBar(max_value=10, orientation='h', size=(45, 15), key='-PGRB-')]
                        ]
    pb_window = sg.Window(title='Loading filter', layout=pb_layout, finalize=True, disable_close=True, modal=True)
    progress_bar = pb_window['-PGRB-']
    progress_bar.update_bar(1)
    choose_filter(filter_name, F_IMG, param_1, param_2, param_3)
    progress_bar.update_bar(6)
    T_IMG = F_IMG.copy()
    T_IMG.thumbnail(size=IMG_SIZE)
    progress_bar.update_bar(8)
    main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
    progress_bar.update_bar(9)
    pb_window.close()   

def choose_filter(filter_name, F_IMG, param_1, param_2, param_3):
    if filter_name == 'Average Grayscale':
        average_grayscale(F_IMG)
    if filter_name == 'Grayscale':
        grayscale(F_IMG)
    if filter_name == 'Luma Grayscale':
        luma_grayscale(F_IMG)
    if filter_name == 'Max and Min Grayscale':
        max_min_grayscale(F_IMG)
    if filter_name == 'Max Grayscale':
        max_grayscale(F_IMG)
    if filter_name == 'Min Grayscale':
        min_grayscale(F_IMG)
    if filter_name == 'Red Grayscale':
        red_grayscale(F_IMG)
    if filter_name == 'Green Grayscale':
        green_grayscale(F_IMG)
    if filter_name == 'Blue Grayscale':
        blue_grayscale(F_IMG)
    if filter_name == 'Shades of Gray':
        shades_of_grayscale(F_IMG, 8)
    if filter_name == 'Brightness':
        brightness(F_IMG, param_1)
    if filter_name == 'Mosaic':
        mosaic(F_IMG, param_1, param_2)
    if filter_name == 'High contrast':
        high_contrast(F_IMG)
    if filter_name == 'Inverted':
        high_contrast(F_IMG, True)
    if filter_name == 'RGB components':
        RGB_components(F_IMG, param_1, param_2, param_3)
    if filter_name == 'Blur':
        blur(F_IMG, param_1)
    if filter_name == 'Motion blur':
        motion_blur(F_IMG)
    if filter_name == 'Find edges':
        find_edges(F_IMG)
    if filter_name == 'Sharpen':
        sharpen(F_IMG)
    if filter_name == 'Emboss':    
        emboss(F_IMG)
    if filter_name == 'Color Ms':
        mosaic(F_IMG, 5, 5, 1)
    if filter_name == 'Grayscale Ms':
        mosaic(F_IMG, 5, 5, 2)
    if filter_name == 'Black and White characters':
        mosaic(F_IMG, 5, 5, 3)
    if filter_name == 'Color characters':
        mosaic(F_IMG, 5, 5, 4)
    if filter_name == 'Grayscale characters':
        mosaic(F_IMG, 5, 5, 5)
    if filter_name == 'Sign':
        mosaic(F_IMG, 10, 10, 9, param_1.upper())
    if filter_name == 'Black dominoes':
        mosaic(F_IMG, 10, 10, 6)
    if filter_name == 'White dominoes':
        mosaic(F_IMG, 10, 10, 7)
    if filter_name == 'Cards':
        mosaic(F_IMG, 10, 10, 8)

start_filter_GUI()
