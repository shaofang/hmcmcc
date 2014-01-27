#!/usr/bin/python
# -*- coding:utf-8 -*- 
import unittest
from devicewrapper.android import device as d
import util as u

class MessageTest(unittest.TestCase):
    def setUp(self):
        super(MessageTest, self).setUp()
        u.setup(d)

    def tearDown(self):
        super(MessageTest, self).tearDown()
        u.teardown(d)

    def testMO_MTSms(self):
        #Set receiver and msg content
        str_receiver = '10086'
        str_content = 'Message Test Content'

        #Start Messaging and check if sucessful
        d.start_activity(component='com.android.mms/.ui.MmsTabActivity')
        assert d(text='New message', className='android.widget.Button').wait.exists(timeout=5000), 'can not launch message in 3s'

        #Delete messages if there is any message.
        if not d(text="No conversations.").wait.exists(timeout=2000):
            d(className='android.view.View').long_click()
            if d(text="Select all").wait.exists(timeout=3000):
                d(text="Select all").click.wait()
            d(text="Delete").click.wait()
            d(text="Delete").click.wait()
            assert d(text="No conversations.").wait.exists(timeout=3000), 'Delete messages failed'

        #Compose message
        d(text='New message').click.wait()
        d(className='android.widget.EditText', index=0).set_text(str_receiver)
        assert d(text=str_receiver).wait.exists(timeout=10000), 'receiver number input error'            
        d(className='android.widget.EditText', index=1).set_text(str_content)
        assert d(text=str_content).wait.exists(timeout=10000), 'content input error'            
        d(descriptionContains='end message').click.wait()
        assert d(text='Received').wait.exists(timeout=20000), 'sms sending failed in 20s'
        #assert d(textStartsWith='尊敬的').wait.exists(timeout=30000), 'No feedback in 30s'

    def testMoMMS(self):
        #Set receiver and msg content
        str_receiver = '13501278511'
        str_content = 'Message Test Content'

        #Start Messaging and check if sucessful
        assert d.exists(text='Messaging') , 'message app not appear on the home screen'
        d(text='Messaging').click.wait()

        #Delete messages if there is any message.
        if not d(text="No conversations.").wait.exists(timeout=1000):
            d(className='android.view.View').long_click()
            if d(text="Select all").wait.exists(timeout=3000):
                d(text="Select all").click.wait()
            d(text="Delete").click.wait()
            d(text="Delete").click.wait()

        #Compose message
        d(text='New message').click.wait()
        d(className='android.widget.EditText', index=0).set_text(str_receiver)
        assert d(text=str_receiver).wait.exists(timeout=10000), 'receiver number input error'            
        d(className='android.widget.EditText', index=1).set_text(str_content)
        assert d(text=str_content).wait.exists(timeout=10000), 'content input error' 

        #Add attachment from camera
        d(descriptionContains='dd attachment').click.wait()

        assert d(text='Capture picture').wait.exists(timeout=3000), 'no adding attachment panel' 
        d(text='Capture picture').click.wait()
        assert d(description='Shutter button').wait.exists(timeout=3000), 'no camera' 
        d(description='Shutter button').click.wait()
        assert d(className='android.widget.ImageView', index=1).wait.exists(timeout=10000), 'Take picture failed'
        d(className='android.widget.ImageView', index=1).click.wait()
        assert d(text='MMS').wait.exists(timeout=5000), 'add attachment failed'

        #Send MMS
        d(descriptionContains='end message').click.wait()
        assert d(text='Sending').wait.exists(timeout=5000), 'No sending status'
        u.sleep(20)
        assert d(text='Sending').wait.gone(timeout=40000), 'MMS sending failed in 60s'



            

