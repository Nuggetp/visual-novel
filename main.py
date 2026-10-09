# json_data["acts"][0]["events"][0]["text"]

import json

import pygame
from dataclasses import dataclass

pygame.init()

#set screen vars
screen_scale = 70
FRAME_RATE = 60
SCREEN_WIDTH = 16*screen_scale
SCREEN_HEIGHT = 9*screen_scale

#colors
BG_COLOR = "#ADF5FF"
TEXT_COLOR = "#247B7B"

#set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Murder on the Ship")

#clock set up
clock = pygame.time.Clock()

act = 1
dialogue_id = 1

with open("data.json", encoding="utf-8") as data_file:
    json_data = json.load(data_file)


def make_text_pages(text: str, font: pygame.font.Font, max_width: int) -> list[list[str]]:
    pages = []
    page = []
    current_line = ""

    for word in text.split():
        next_line = word if not current_line else f"{current_line} {word}"
        if current_line and font.size(next_line)[0] > max_width:
            page.append(current_line)
            current_line = word
        else:
            current_line = next_line

        if len(page) == 3:
            pages.append(page)
            page = []

    if current_line:
        page.append(current_line)
    if page:
        pages.append(page)
    if not pages:
        pages.append([])

    return [page + [" "] * (3 - len(page)) for page in pages]


@dataclass
class TextBox:
    height: int = 250
    width: int = SCREEN_WIDTH
    x: int = 0
    y: int = SCREEN_HEIGHT-height
    text: str = ""
    font: pygame.font.Font = pygame.font.Font("game_text.ttf", 50)

    def write(self, text:list, speaker):
        textbox_rect = pygame.Surface((self.width, self.height))
        textbox_rect.fill(BG_COLOR)

        outline = pygame.Rect(0,0, self.width, self.height)
        pygame.draw.rect(textbox_rect, TEXT_COLOR, outline, width=10) 
        screen.blit(textbox_rect, (self.x, self.y))


        #text writing
        char_amount = 3*len(text[0])

        if len(text) > char_amount:
            return 0

        else:
            for line_number, line in enumerate(text[:3]):
                rendered_line = self.font.render(line, True, TEXT_COLOR)
                screen.blit(
                    rendered_line,
                    (self.x + 40, self.y + 20 + line_number * 50),
                )
            

        

#main loop
def mainloop():
    global clock, screen, act, dialogue_id

    textbox = TextBox()
    current_event = json_data["acts"][act-1]["events"][dialogue_id-1]
    current_pages = []
    if current_event["type"] == "dialogue":
        current_pages = make_text_pages(current_event["text"], textbox.font, textbox.width - 80)
    running = True
    page_on = 0

    while running:
        screen.fill(BG_COLOR)
        if current_event["type"] == "dialogue":
            textbox.write(current_pages[page_on], current_event["speaker"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if page_on < len(current_pages) - 1:
                    page_on += 1
                else:
                    if len(json_data['acts'][act-1]['events']) <= dialogue_id:
                        act += 1
                        dialogue_id = 1
                        page_on = 0

                    else:
                        page_on = 0
                        dialogue_id += 1
                    current_event = json_data["acts"][act-1]["events"][dialogue_id-1]
                    if current_event['type'] == "dialogue":
                        current_pages = make_text_pages(current_event["text"], textbox.font, textbox.width - 80)
                    elif current_event['type'] == 'choice event':
                        pass
                    

        clock.tick(FRAME_RATE)
        pygame.display.flip()

if __name__ == "__main__":
    mainloop()
    pygame.quit()