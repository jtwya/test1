# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MBRNcqs--DjYDVVnsHHJeiPJwSR8cfvy
"""

import os

from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage, ConfirmTemplate, MessageAction,
    CarouselTemplate,CarouselColumn,URIAction,PostbackAction
)

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('Line_Channel_access_token'))
line_handler = WebhookHandler(os.getenv('Line_Channel_secret'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

import google.generativeai as genai
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')
def ask_gemini(question):
  response = model.generate_content(question)
  return response.text

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        action = event.message.text
        print(f"Action: {action}")
        if action == 'strange food':
          print(f"Action: {action}")
          Carrousel_template = CarouselTemplate(
              columns = [
                  CarouselColumn(
                      thumbnail_image_url = 'https://stickershop.line-scdn.net/stickershop/v1/product/19786399/LINEStorePC/main.png?v=1',
                      title = '莫帕尼蠕蟲，南非',
                      text = '帝王蛾的幼蟲，敢挑戰嗎?',
                      actions = [
                          URIAction(label='它長怎樣?', uri='https://imgs.gvm.com.tw/upload/gallery/20250424/202112.jpg'),
                          URIAction(label='維基百科', uri='https://en.wikipedia.org/wiki/Gonimbrasia_belina'),
                          MessageAction(label="想知道更多", text="想知道有關南非的莫帕尼蠕蟲的事!")
                          ]
                      ),
                  CarouselColumn(
                      thumbnail_image_url = 'https://www.niusnews.com/upload/imgs/default/2021SEP_CHOU/0908Emoji/4.jpg',
                      title = '哈卡爾，冰島',
                      text = '發酵鯊魚想嘗試嗎?',
                      actions = [
                          URIAction(label='它長怎樣?', uri='https://imgs.gvm.com.tw/upload/gallery/20250424/202121.jpg'),
                          URIAction(label='維基百科', uri='https://zh.wikipedia.org/zh-tw/%E5%93%88%E5%8D%A1%E7%88%BE'),
                          MessageAction(label="想知道更多", text="想知道有關冰島的哈卡爾的事!")
                          ]
                      ),
                  CarouselColumn(
                      thumbnail_image_url = 'https://cdn2.ettoday.net/images/423/c423263.jpg',
                      title = '卡蘇馬蘇起司，義大利',
                      text = '被活蛆感染的起司你敢吃嗎？',
                      actions = [
                          URIAction(label='它長怎樣?', uri='https://imgs.gvm.com.tw/upload/gallery/20250424/202115.jpg'),
                          URIAction(label='維基百科', uri='https://zh.wikipedia.org/zh-tw/%E5%8D%A1%E8%98%87%E9%A6%AC%E8%98%87%E4%B9%B3%E9%85%AA'),
                          MessageAction(label="想知道更多", text="想知道有關義大利的卡蘇馬蘇起司的事!")
                          ]
                      )
                  ]
              )
          reply = TemplateMessage(
              alt_text="這是輪播視窗",
              template=Carrousel_template
              )
        else:
          print("Action is not 'strange food'")
          reply = TextMessage(text="Thanks")
          response = ask_gemini(event.message.text)
          reply = TextMessage(text=response)

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[reply]
                )
              )




if __name__ == "__main__":
    app.run()