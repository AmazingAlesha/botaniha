import shutil
import torch
import telebot

model = torch.hub.load('ultralytics/yolov5', 'custom', path='E:/botTG/model_pmik.pt', force_reload=True)

bot = telebot.TeleBot('6259719229:AAFIqVU3SeHAiy01u1U89XSIdOR5M3ukGMI')

mass = ['кота (ну или кошку)','собаку','обезьянку']

def len_space (argument, lenarg):
    i = 0
    argument = argument[lenarg:]
    while (i<len(argument)):
        if argument[i] == ' ':
            i += 1
        else: return i


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, отправь мне фото или картинку')

@bot.message_handler(content_types=['photo','video'])
def handler_file(message):
    from pathlib import Path
    Path(f'files/photos/').mkdir(parents=True, exist_ok=True)
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'files/photos/' + file_info.file_path.replace('photos/', '')
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, f'Думою...')
        imgs = src
        results = model(imgs)
        cls = str(results.xyxyn[0][:, -1].numpy())
        cls = cls[1:-1]
        koord = str(results.pandas().xyxy[0])
        koordpr = koord.split('\n')[0]
        len(koordpr)
        koord = koord[len(koordpr)+1:]
        i = 0
        chek = 0
        while (i < len(cls)):
            if cls[i] != ' ':
                chek = 1
                index = int(cls[i])
                koordprint = koord.split('\n')[0]
                l = len(koordprint)
                element = koordprint
                el1 = element.split(' ')[0]
                element = element[len(el1) + len_space(element,len(el1)):]
                el1 = int(el1)
                el1 +=1
                el2 = element.split(' ')[0]
                element = element[len(el2) + len_space(element, len(el2)):]
                el3 = element.split(' ')[0]
                element = element[len(el3) + len_space(element, len(el3)):]
                el4 = element.split(' ')[0]
                element = element[len(el4) + len_space(element, len(el4)):]
                el5 = element.split(' ')[0]
                element = element[len(el5) + len_space(element, len(el5)):]
                el6 = element.split(' ')[0]
                bot.send_message(message.chat.id, f'Я нашел {mass[index]}\nОбъект №{el1} Вероятность совпадения: {el6}\nКоординаты: [ Xmin: {el2};  Ymin: {el3};  Xmax: {el4};  Ymax: {el5} ]')
                koord = koord[l+1:]
            i += 1
        if chek == 0:
            bot.send_message(message.chat.id, f'Я никого не нашёл :с\n{message.from_user.first_name}, давай попробуем с другми изображением')
        srcout = f'files/detect/'
        results.save(save_dir=srcout)
        if chek == 1:
            bot.send_photo(message.chat.id, open(srcout + file_info.file_path.replace('photos/', ''), 'rb'))
            #print(results.pandas().xyxy[0])
            bot.send_message(message.chat.id, f'{message.from_user.first_name}, можем попробовать еще раз :3')
        path = f'files/'
        shutil.rmtree(path)

bot.polling(none_stop=True)