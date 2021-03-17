# pylint: disable=no-member
import PySimpleGUI as sg
import io
import os
from PIL import Image, ImageGrab
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
                             '&Convolution', ['&Blur', '&Motion blur', '&Find edges' , '&Sharpen'

                                             ]
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
                pb_window = sg.Window(title='Loading filter', layout=pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                average_grayscale(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()                

            elif event == 'Grayscale':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                grayscale(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()

            elif event == 'Luma Grayscale':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                luma_grayscale(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()
            
            elif event == 'Max and Min Grayscale':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                max_min_grayscale(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()
            
            elif event == 'Max Grayscale':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                max_grayscale(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()
            
            elif event == 'Min Grayscale':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                min_grayscale(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()
            
            elif event == 'Red Grayscale':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                red_grayscale(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()
            
            elif event == 'Green Grayscale':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                green_grayscale(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()

            elif event == 'Blue Grayscale':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                blue_grayscale(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()

            elif event == 'Shades of Gray':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                shades_of_grayscale(F_IMG, 8)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()
            
            elif event == 'Brightness':
                
                b_event, b_values = sg.Window('Brightness', [
                    [sg.T('Adjust brightness')],
                    [sg.Slider(range=(-180, 180), default_value=0, resolution=1, tick_interval=100, 
                                orientation='h', border_width=3, size=(40, 10), key='-BRGHT-', tooltip='Brightness')],
                    [sg.Button('Ok')]
                ], modal=True, keep_on_top=True).read(close=True)
                brightness_value = b_values['-BRGHT-']
                if brightness_value != None:
                    pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                    progress_bar = pb_window['-PGRB-']
                    F_IMG = OG_IMG.copy()
                    progress_bar.update_bar(1)
                    brightness(F_IMG, int(brightness_value))
                    progress_bar.update_bar(6)
                    T_IMG = F_IMG.copy()
                    T_IMG.thumbnail(size=IMG_SIZE)
                    progress_bar.update_bar(8)
                    main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                    progress_bar.update_bar(9)
                    pb_window.close()

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
                    pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                    progress_bar = pb_window['-PGRB-']
                    F_IMG = OG_IMG.copy()
                    progress_bar.update_bar(1)
                    mosaic(F_IMG, int(w_value), int(h_value))
                    progress_bar.update_bar(6)
                    T_IMG = F_IMG.copy()
                    T_IMG.thumbnail(size=IMG_SIZE)
                    progress_bar.update_bar(8)
                    main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                    progress_bar.update_bar(9)
                    pb_window.close()

            elif event == 'High contrast':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                high_contrast(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()
            
            elif event == 'Inverted':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                high_contrast(F_IMG, True)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()

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
                
                    pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                    progress_bar = pb_window['-PGRB-']
                    F_IMG = OG_IMG.copy()
                    progress_bar.update_bar(1)
                    RGB_components(F_IMG, int(red), int(green), int(blue))
                    progress_bar.update_bar(6)
                    T_IMG = F_IMG.copy()
                    T_IMG.thumbnail(size=IMG_SIZE)
                    progress_bar.update_bar(8)
                    main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                    progress_bar.update_bar(9)
                    pb_window.close()
            
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
                    pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                    progress_bar = pb_window['-PGRB-']
                    F_IMG = OG_IMG.copy()
                    progress_bar.update_bar(1)
                    blur(F_IMG, selection)
                    progress_bar.update_bar(6)
                    T_IMG = F_IMG.copy()
                    T_IMG.thumbnail(size=IMG_SIZE)
                    progress_bar.update_bar(8)
                    main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                    progress_bar.update_bar(9)
                    pb_window.close()
            
            elif event == 'Motion blur':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                motion_blur(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()
            
            elif event == 'Find edges':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                find_edges(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()
            
            elif event == 'Sharpen':
                pb_window = sg.Window('Loading filter', pb_layout, finalize=True, disable_close=True, modal=True)
                progress_bar = pb_window['-PGRB-']
                F_IMG = OG_IMG.copy()
                progress_bar.update_bar(1)
                sharpen(F_IMG)
                progress_bar.update_bar(6)
                T_IMG = F_IMG.copy()
                T_IMG.thumbnail(size=IMG_SIZE)
                progress_bar.update_bar(8)
                main_window['-F_IMAGE-'].update(data=get_bytes(T_IMG), size=IMG_SIZE)
                progress_bar.update_bar(9)
                pb_window.close()

        if event == 'About...':
            #main_window.disappear()
            sg.popup('Filter App', 'Version 1.01', 'Carlos Eduardo Orozco Viveros', 'Release date: 03/12/21',
                     grab_anywhere=True, modal=True, 
                     background_color=MAIN_COLOR, text_color=TXT_COLOR, no_titlebar=True)
            #main_window.reappear()

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

start_filter_GUI()
