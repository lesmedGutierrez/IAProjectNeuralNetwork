import pygame.font, pygame.event, pygame.draw
from PIL import Image
from Models import neural_network as neu_net

def cropImage(Image):
    row = Image.size[0]
    col = Image.size[1]
    print(str(row)+"x"+str(col))
    #t=top r=right b=bottom l=left
    to = ri = bo = le = 0
    suml = 0
    sumr = 0
    flag = 0
    pixels = Image.load()
    print(pixels[0, 0])
    #/**************************top edge***********************/
    for x in range(row):
        for y in range(col):
            r = pixels[x, y][0]
            g = pixels[x, y][1]
            b = pixels[x, y][2]
            if(((r+g+b)/3)<=200):
                flag = 1
                to = x
                break
        if(flag==1):
            flag = 0
            break
    #/*******************bottom edge***********************************/
    for x in range(row-1, 0, -1):
        for y in range(col):
            r = pixels[x, y][0]
            g = pixels[x, y][1]
            b = pixels[x, y][2]
            if(((r+g+b)/3)<=200):
                flag = 1
                bo = x
                break
        if(flag==1):
            flag = 0
            break
    #/*************************left edge*******************************/

    for y in range(col):
        for x in range(row):
            r = pixels[x, y][0]
            g = pixels[x, y][1]
            b = pixels[x, y][2]
            if(((r+g+b)/3)<=200):
                flag = 1
                le = y
                break
        if(flag==1):
            flag = 0
            break

    #/**********************right edge***********************************/
    for y in range(col-1, 0, -1):
        for x in range(row):
            r = pixels[x, y][0]
            g = pixels[x, y][1]
            b = pixels[x, y][2]
            if(((r+g+b)/3)<=200):
                flag = 1
                ri = y
                break
        if(flag==1):
            flag = 0
            break
    box = (to, le, bo, ri)
    img = Image.crop(box)
    return img

def main():
    """Main method. Draw interface"""
    net = neu_net.NeuralNetwork()
    global screen
    pygame.init()
    screen = pygame.display.set_mode((350, 350))
    pygame.display.set_caption("Handwriting recognition")

    background = pygame.Surface((350,350))
    background.fill((255, 255, 255))

    clock = pygame.time.Clock()
    keepGoing = True
    lineStart = (0, 0)
    drawColor = (0, 0, 0)
    lineWidth = 5
    pygame.display.update()

    while keepGoing:

        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEMOTION:
                lineEnd = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    pygame.draw.line(background, drawColor, lineStart, lineEnd, lineWidth)
                lineStart = lineEnd
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    data = pygame.image.tostring(background, 'RGB')
                    img = Image.fromstring('RGB', (350,350), data)
                    img = cropImage(img)
                    #img.show()
                    #img.save("crop_image.png", 'PNG')
                    img = img.resize((30, 30), Image.ANTIALIAS)
                    pixels = img.load()
                    input = []
                    for i in range(img.size[0]):    # for every pixel:
                        for j in range(img.size[1]):
                            r = pixels[j,i][0]
                            g = pixels[j,i][1]
                            b = pixels[j,i][2]
                            if(((r+g+b)/3)>230):

                                input.append(1)
                                pixels[j,i] = (255,255,255)
                            elif(((r+g+b)/3)<=230):
                                input.append(0)
                                pixels[j,i] = (0,0,0)

                    img.save("../imagen.png", 'PNG')
                    net.feed_forward([input])
                elif event.key == pygame.K_c:
                    background = pygame.Surface((350, 350))
                    background.fill((255, 255, 255))

        screen.blit(background, (0, 0))
        pygame.display.flip()