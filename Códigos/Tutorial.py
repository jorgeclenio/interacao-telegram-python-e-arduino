# !/usr/bin/python
# -*- coding: utf-8 -*-

import telepot
import traceback
import Arduino


# VARIAVEIS PARA ENVIAR AO ARDUINO DEPENDENDO DO COMANDO
ACTIVATE_LED = b'1'
DEACTIVATE_LED = b'0'

class TelegramTutorial(telepot.Bot):
    def __init__(self, token):
        super(TelegramTutorial, self).__init__(token)
        self.serial = Arduino.start_communication()

    def handle_message(self, msg):
        if 'text' not in msg:
            return

        if msg['text'].startswith('/'):
            self.handle_command(msg)

    def handle_start(self, msg):
        self.sendMessage(msg['chat']['id'], "Seja muito bem vindo, chefe. O que deseja fazer?")

    def handle_ligarLed(self, msg):
        self.sendMessage(msg['chat']['id'], "Ligando LED")

        self.serial.write(ACTIVATE_LED)

        response = self.serial.readline()

        if not response:
            response = 'Nenhuma resposta recebida'
        else:
            response = 'Perfeito chefe, ' + response.decode('utf-8')

        self.sendMessage(msg['chat']['id'], response)

    def handle_desligarLed(self, msg):
        self.sendMessage(msg['chat']['id'], "Desligando LED")

        self.serial.write(DEACTIVATE_LED)

        response = self.serial.readline()

        if not response:
            response = 'Nenhuma resposta recebida'
        else:
            response = 'Perfeito chefe, ' + response.decode('utf-8')

        self.sendMessage(msg['chat']['id'], response)

    def handle_command(self, msg):

        method = 'handle_' + msg['text'][1:]

        if hasattr(self, method):
            getattr(self, method)(msg)

    def runBot(self):
        last_offset = 0
        print('Ouvindo...')

        while True:
            try:
                updates = self.getUpdates(timeout=60, offset=last_offset)

                if updates:
                    for u in updates:
                        self.handle_message(u['message'])

                    last_offset = updates[-1]['update_id'] + 1

            except KeyboardInterrupt:
                break
            except:
                traceback.print_exc()