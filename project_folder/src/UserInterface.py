import PySimpleGUI as sg
from main import summarize_wrapper
from Summarization import output_format_gui
from fpdf import FPDF


def summarizeWindow():
    # window layout
    sg.theme('Dark')
    layout = [
        [sg.Titlebar('Summarization Application')],
        [sg.Text('Filename')],
        [sg.InputText(), sg.FileBrowse()],
        [sg.Submit('Summarize'), sg.Cancel()],
        [],
        [sg.Text('Summarized data')],
        [sg.Multiline(key='-OUTPUT-', size=(400, 10))],
        [sg.Text('Save summarized data as PDF')],
        [sg.InputText(key='pdfname'), sg.FolderBrowse('Choose Folder'), sg.Button('Save as PDF')]
    ]
    # creates window
    window = sg.Window('PDF Summarizer', layout, size=(600, 600))
    while True:
        event, values = window.read()

        if event == 'Cancel':
            window.close()
            main()

        if event == 'Summarize':
            try:
                path = values['Browse']
                summary = output_format_gui(summarize_wrapper(path))
                window['-OUTPUT-'].update(summary)
            # summariser does not work as the file is too small
            except (IndexError):
                sg.popup_error('File too small')
            # handles all other exceptions (when file is not a pdf)
            except:
                sg.popup_error('Not a PDF')

        # save the summarized data as a PDF
        if event == 'Save as PDF':
            try:
                # the path for where you want to save the PDF
                pdfname = values['pdfname']

                # creates PDF object
                pdf = FPDF('P', 'mm', 'Letter')
                pdf.add_page()
                pdf.set_font('times', '', 12)

                # decoding to latin-1 was necessary to create PDF
                utf8 = summary.encode()
                txt = utf8.decode('latin-1')
                pdf.multi_cell(0, 5, txt)
                pdf.ln()

                # creates the PDF file
                pdf.output(pdfname)
                sg.popup_timed('Saved as PDF!')
            except:
                sg.popup_error('No summarized data received')

        if event == sg.WINDOW_CLOSED:
            break
    window.close(); del window

def main():
    # window layout
    sg.theme('Dark')
    layout = [
        [sg.Titlebar('Our App')],
        [sg.Text('Pick an Option')],
        [sg.Button('Summarize'), sg.Cancel('Close App')],
    ]

    window = sg.Window('PDF Summarizer', layout, size=(500, 500))

    while True:
        event, values = window.read()
        # closes app
        if event == 'Close App' or event == sg.WINDOW_CLOSED:
            break
        # goes to summarization window
        if event == 'Summarize':
            window.close()
            summarizeWindow()

    window.close(); del window


if __name__ == '__main__':
    main()
