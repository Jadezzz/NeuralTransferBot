from transitions.extensions import GraphMachine
from my_utils import *
from evaluate import transfer
import requests
class MyMachine(GraphMachine):
    def __init__(self):
        self.machine = GraphMachine(
        model = self,
        states = [
            'Init',
            'Welcome',
            'Transfer',
            'Style',
            'Image',
            'Finish',
            'About',
            'Example'
        ],
        transitions = [
            {
                'trigger' : 'advance',
                'source' : 'Init',
                'dest' : 'Welcome',
                'conditions' : 'is_going_to_Welcome'
            },
            {
                'trigger' : 'advance',
                'source' : 'Welcome',
                'dest' : 'Transfer',
                'conditions' : 'is_going_to_Transfer'
            },
            {
                'trigger' : 'advance',
                'source' : 'Transfer',
                'dest' : 'Style',
                'conditions' : 'is_going_to_Style'
            },
            {
                'trigger' : 'advance',
                'source' : 'Style',
                'dest' : 'Image',
                'conditions' : 'is_going_to_Image'
            },
            {
                'trigger' : 'advance',
                'source' : 'Image',
                'dest' : 'Finish'
            },
            {
                'trigger' : 'advance',
                'source' : 'Welcome',
                'dest' : 'About',
                'conditions' : 'is_going_to_About'
            },
            {
                'trigger' : 'advance',
                'source' : 'Welcome',
                'dest' : 'Example',
                'conditions' : 'is_going_to_Example'
            },
            {
                'trigger' : 'go_back',
                'source' : [
                    'Finish',
                    'About',
                    'Example'
                ],
                'dest' : 'Init'
            }   
        ],
        initial = 'Init',
        auto_transitions = False,
        show_conditions = True,
        )
        self.style_path = ''
        self.selected = -1
        self.styles = ['la_muse', 'rain_princess', 'scream', 'udnie', 'wave']
        self.input_path = '/var/www/NeuralTransferBot/content/input.jpg'
        self.output_path = '/var/www/NeuralTransferBot/output/out.jpg'
    
    def is_going_to_Welcome(self, event):
        if 'message' in event:
            if 'text' in event['message']:
                if event['message']['text'] == 'Hi':
                    return True
        return False

    def is_going_to_Transfer(self, event):
        if event.get('postback'):
            if event['postback']['payload'] == 'Start!':
                return True
        pass

    def is_going_to_Style(self, event):
        sender_id = event['sender']['id']
        if 'message' in event:
            if 'text' in event['message']:
                choice = event['message']['text']
                if choice == '1':
                    self.selected = 1
                    self.style_path = '/var/www/NeuralTransferBot/checkpoints/la_muse.ckpt'
                elif choice == '2':
                    self.selected = 2
                    self.style_path = '/var/www/NeuralTransferBot/checkpoints/rain_princess.ckpt'
                elif choice == '3':
                    self.selected = 3
                    self.style_path = '/var/www/NeuralTransferBot/checkpoints/scream.ckpt'
                elif choice == '4':
                    self.selected = 4
                    self.style_path = '/var/www/NeuralTransferBot/checkpoints/udnie.ckpt'
                elif choice == '5':
                    self.selected = 5
                    self.style_path = '/var/www/NeuralTransferBot/checkpoints/wave.ckpt'
                else:
                    send_text_message(sender_id, "Please choose a style from 1~5!")
                    return False
                text = "The style you chose is " + self.styles[self.selected - 1]
                send_text_message(sender_id, text)
                return True
    
    def is_going_to_Image(self, event):
        sender_id = event['sender']['id']
        if 'message' in event:
            if 'attachments' in event['message']:
                if event['message']['attachments'][0]['type'] == 'image':
                    img_url = event['message']['attachments'][0]['payload']['url']
                    save_img(img_url)
                    #print(img_url)
                    return True
        send_text_message(sender_id, "Please upload an image!")
        return False

    def is_going_to_About(self, event):
        if event.get('postback'):
            if event['postback']['payload'] == 'About':
                return True
        return False
    
    def is_going_to_Example(self, event):
        if event.get('postback'):
            if event['postback']['payload'] == 'Examples':
                return True
        return False

    def on_enter_Welcome(self, event):
        print(self.state)
        sender_id = event['sender']['id']
        send_welcome_template(sender_id)
    
    def on_enter_Transfer(self, event):
        print(self.state)
        sender_id = event['sender']['id']
        text = "Step1:Choose a style!\n(Enter the number of the style)"
        send_text_message(sender_id, text)
        text = "Style 1 (la_muse)"
        send_text_message(sender_id, text)
        send_attachment(sender_id, get_image_id(1))
        text = "Style 2 (rain_princess)"
        send_text_message(sender_id, text)
        send_attachment(sender_id, get_image_id(2))
        text = "Style 3 (the_scream)"
        send_text_message(sender_id, text)
        send_attachment(sender_id, get_image_id(3))
        text = "Style 4 (udnie)"
        send_text_message(sender_id, text)
        send_attachment(sender_id, get_image_id(4))
        text = "Style 5 (wave)"
        send_text_message(sender_id, text)
        send_attachment(sender_id, get_image_id(5))

    
    def on_enter_About(self, event):
        print(self.state)
        sender_id = event['sender']['id']
        send_website_template(sender_id)
        self.go_back(event)

    def on_enter_Example(self, event):
        print(self.state)
        sender_id = event['sender']['id']
        send_text_message(sender_id, "Given a style")
        send_attachment(sender_id, get_image_id(4))
        send_text_message(sender_id, "Given an image")
        send_attachment(sender_id, get_image_id(6))
        send_text_message(sender_id,"I can repaint the image!")
        send_attachment(sender_id, get_image_id(7))
        self.go_back(event)
    
    def on_enter_Style(self, event):
        print(self.state)
        sender_id = event['sender']['id']
        send_text_message(sender_id, "Please upload an image!")
    
    def on_enter_Image(self, event):
        print(self.state)
        sender_id = event['sender']['id']
        send_text_message(sender_id, "Transferring! Please wait ...")
        transfer(self.input_path, self.output_path, self.style_path)
        send_img(sender_id, "/var/www/NeuralTransferBot/output/out.jpg")
        self.advance(event)

    def on_enter_Finish(self, event):
        print(self.state)
        sender_id = event['sender']['id']
        send_text_message(sender_id, "Thank you for using!")
        self.go_back(event)
    
    def on_enter_Init(self, event):
        print(self.state)
