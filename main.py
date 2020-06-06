from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock


class Mesa(Widget):
    ponto = NumericProperty(0)

    def movimento_bolinha(self, bola):
        if self.collide_widget(bola):
            vx, vy = bola.velocidade
            deslocamento = (bola.center_y - self.center_y) / (self.height / 2)
            movimento = Vector(-1 * vx, vy)
            vel = movimento * 1.1
            bola.velocidade = vel.x, vel.y + deslocamento


class PingPongBolinha(Widget):
    velocidade_x = NumericProperty(0)
    velocidade_y = NumericProperty(0)
    velocidade = ReferenceListProperty(velocidade_x, velocidade_y)

    def move(self):
        self.pos = Vector(*self.velocidade) + self.pos


class PingPongGame(Widget):
    bola = ObjectProperty(None)
    jogador1 = ObjectProperty(None)
    jogador2 = ObjectProperty(None)

    def velocidade_bola(self, vel=(4, 0)):
        self.bola.center = self.center
        self.bola.velocidade = vel

    def update(self, dt):
        self.bola.move()

        self.jogador1.movimento_bolinha(self.bola)
        self.jogador2.movimento_bolinha(self.bola)

        if (self.bola.y < self.y) or (self.bola.top > self.top):
            self.bola.velocidade_y *= -1

        if self.bola.x < self.x:
            self.jogador2.ponto += 1
            self.velocidade_bola(vel=(4, 0))
        if self.bola.x > self.width:
            self.jogador1.ponto += 1
            self.velocidade_bola(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.jogador1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.jogador2.center_y = touch.y


class PingPongApp(App):
    def build(self):
        game = PingPongGame()
        game.velocidade_bola()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PingPongApp().run()
