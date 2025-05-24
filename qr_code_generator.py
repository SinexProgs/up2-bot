from io import BytesIO
import qrcode
import bot


def generate_qr_code(text):
    img = qrcode.make(text)

    bytes_io = BytesIO()
    bytes_io.name = "qr_code.jpeg"

    img.save(bytes_io, 'JPEG')

    bytes_io.seek(0)
    return bytes_io


def enter_qr_code_generator_state(message):
    bot.set_bot_state(message, bot.BotStates.qr_code_generator)
    bot.bot.send_message(message.chat.id,
                         text="Введите текст для преобразования в QR код.",
                         reply_markup=bot.cancel_keyboard)