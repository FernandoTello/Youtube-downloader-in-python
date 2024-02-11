from pytube import YouTube
import flet as ft
import os
import paths
from time import sleep

def main(page: ft.Page):
    # Page setup
    page.title = 'Youtube Download'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_center()
    page.window_width = 400
    page.window_height = 400

    # Define function to handle button click event
    def button_clicked(e):
        page.controls.clear()
        try:
            yt = YouTube(URL.value)

            # Create controls to display download information
            text = ft.Text('Downloading...')
            title = ft.Text(yt.title)
            pb = ft.ProgressBar(width=400)
            thumbnail = ft.Image(src=yt.thumbnail_url,
                                 width=200,
                                 height=200,
                                border_radius=ft.border_radius.all(10)
                                )
            page.add(
                title,
                thumbnail,
                text,
                pb
            )
            page.update()

            # Download the video
            if format.value == 'mp3':
                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download(output_path=paths.AUDIO_PATH)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
            elif format.value == 'mp4':
                video = yt.streams.get_highest_resolution()
                out_file = video.download(output_path=paths.VIDEO_PATH)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp4'
            os.rename(out_file, new_file)
            
            # Update UI after download
            text.value = 'Download finished'
            page.controls.pop()
            page.update()
        except Exception as e:
            print('Error:', type(e).__name__, '-', e)
            # Show error message in UI
            page.add(ft.Text('Error occurred during download'))
        
        # Clear controls after some time
        sleep(2)
        page.controls.clear()
        page.add(URL, submit, format)
        page.update()

    # Create UI controls
    URL = ft.TextField(label='URL', autofocus=True)
    submit = ft.ElevatedButton('Download', on_click= button_clicked)
    format = ft.RadioGroup(content=ft.Column([
        ft.Radio(value='mp4', label='mp4'),
        ft.Radio(value='mp3', label='mp3')
    ]))

    page.add(URL, submit, format)
    
# Start the application
ft.app(target=main)
