import telebot
from instagrapi import Client
import pyshorteners

bot = telebot.TeleBot("5471405122:AAGyoP6IdfDAoTwouPdjYyegfXIvjhxL-n8")
cl = Client()
user = ['YOUR INSTAGRAM USER NAME']
password = ['YOUR PASSWORD']
cl.login(user, password)
type_tiny = pyshorteners.Shortener()



@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello\nYou can download from instagram(story,post,reels,igtv,profile picture)\nIf you want to get an instagram user's profile picture enter it in this format:\n:username\nOtherwise just enter the url")


@bot.message_handler(func=lambda msg: True)
def download(message):
  txt = message.text
  res = 'Unavailable link'
  if 'instagram' in txt:
      if 'stories' in txt:
          s = cl.story_pk_from_url(txt)
          story = cl.story_info(s).dict()
          if story['video_url']:
              res = type_tiny.tinyurl.short(story['video_url'])
          elif story['thumbnail_url']:
              res = type_tiny.tinyurl.short(story['thumbnail_url'])
      elif '/p/' in txt or '/tv/' in txt or '/reel/' in txt:
          media_pk = cl.media_pk_from_url(txt)
          media_type = cl.media_info(media_pk).dict()['media_type']
          if media_type == 2:
              post = cl.media_info(media_pk).dict()['video_url']
              res = type_tiny.tinyurl.short(post)
          elif media_type == 1:
              image = cl.media_info(media_pk).thumbnail_url
              res = type_tiny.tinyurl.short(image)
          elif media_type == 8:
              for item in cl.media_info(media_pk).dict()['resources']:
                  if item['video_url'] == None:
                      alb = item['thumbnail_url']
                      res = type_tiny.tinyurl.short(alb)
                      bot.send_message(chat_id=message.chat.id , text=res)
                  else:
                      album = item['video_url']
                      res = type_tiny.tinyurl.short(album)
                      bot.send_message(chat_id=message.chat.id , text=res)
              res = 'q'
  elif txt[0] == ':':
      try:
          profile = cl.user_info_by_username(txt[1:]).dict()
          res = type_tiny.tinyurl.short(profile['profile_pic_url'])
      except:
          res = 'User not found'
  if res != 'q':
    bot.send_message(chat_id=message.chat.id , text=res)

bot.infinity_polling()
