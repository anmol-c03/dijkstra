from tkinter import messagebox, Tk
import pygame
import sys

from properties import Properties
from box import Box


class VisualizerApp:
    def __init__(self):
        self.properties = Properties()
        pygame.init()
        self.window = pygame.display.set_mode(
            (self.properties.window_width, self.properties.window_height))
        pygame.display.set_caption("VISUALIZER.ALGO")
        game_icon = pygame.image.load('images/gameicon.jpg')
        pygame.display.set_icon(game_icon)
        self._init_images()
        self.grid = []
        self._createGrid()
        self.start_box = Box(self, -1, -1)
        self.target_box = Box(self, -1, -1)
        self.target_loc = []
        self.start_loc = []
        self.start_box_set = False
        self.target_box_set = False
        self.begin_search = False
        self.queue = []

    def _init_images(self):
        self.start_icon = pygame.image.load('images/home.png')
        self.start_icon = pygame.transform.scale(
            self.start_icon, (self.properties.box_width, self.properties.box_height))
        self.target_icon = pygame.image.load('images/target.png')
        self.target_icon = pygame.transform.scale(
            self.target_icon, (self.properties.box_width, self.properties.box_height))

    def _createGrid(self):
        for i in range(self.properties.columns):
            arr = []
            for j in range(self.properties.rows):
                arr.append(Box(self, i, j))
            self.grid.append(arr)

    def RunApp(self):

        while True:
            self._checkevents()
            self._updatescreen()

    def _checkevents(self):
        for event in pygame.event.get():
            # quit window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # allows drag n draw
            elif event.type == pygame.MOUSEMOTION:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                if event.buttons[0]:
                    self._mouse_event_leftclick(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                if pygame.mouse.get_pressed()[0]:
                    self._mouse_event_leftclick(mouse_x, mouse_y)
                elif pygame.mouse.get_pressed()[2]:
                    self._mouse_event_rightclick(mouse_x, mouse_y)
            # start algorithm
            if event.type == pygame.KEYDOWN and self.target_box_set:
                self.begin_search = True

    def _mouse_event_leftclick(self, x, y):
        index_i = x // self.properties.box_width
        index_j = y // self.properties.box_height
        if not self.start_box_set:
            # draw start
            self.start_box = self.grid[index_i][index_j]
            self.grid[index_i][index_j].start = True
            self.start_loc.append(index_i)
            self.start_loc.append(index_j)
            self.start_box.start = True
            self.start_box_set = True
        else:
            # draw wall, toggles the state
            if not self.grid[index_i][index_j].target:
                if not self.grid[index_i][index_j].start:
                    self.grid[index_i][index_j].wall = True

    def _mouse_event_rightclick(self, x, y):
        index_i = x // self.properties.box_width
        index_j = y // self.properties.box_height
        if not self.target_box_set:
            self.target_box = self.grid[index_i][index_j]
            self.grid[index_i][index_j].target = True
            self.target_loc.append(index_i)
            self.target_loc.append(index_j)
            self.target_box.target = True
            self.target_box_set = True

    def _updatescreen(self):
        self.window.fill(self.properties.bg_color)
        self._drawGrid()
        if self.start_box_set:
            self._draw_starticon()
        if self.target_box_set:
            self._draw_targeticon()
        pygame.display.flip()

    def _drawGrid(self):
        for i in range(self.properties.columns):
            for j in range(self.properties.rows):
                box = self.grid[i][j]
                box.draw()

    def _draw_starticon(self):
        if self.start_loc:
            start_rect = self.start_icon.get_rect()
            start_rect.left = self.window.get_rect(
            ).left + self.start_loc[0] * self.properties.box_width
            start_rect.top = self.window.get_rect(
            ).top + self.start_loc[1] * self.properties.box_height
            self.window.blit(self.start_icon, start_rect)

    def _draw_targeticon(self):
        if self.target_loc:
            target_rect = self.target_icon.get_rect()
            target_rect.left = self.window.get_rect(
            ).left + self.target_loc[0] * self.properties.box_width
            target_rect.top = self.window.get_rect(
            ).top + self.target_loc[1] * self.properties.box_height
            self.window.blit(self.target_icon, target_rect)


if __name__ == '__main__':
    visualizerapp = VisualizerApp()
    visualizerapp.RunApp()