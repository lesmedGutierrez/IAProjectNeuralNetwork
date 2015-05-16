import pygame.font, pygame.event, pygame.draw
from PIL import Image
from Models import neural_network as neu_net
import pickle as pck
from os.path import abspath, exists
import glob



def Process_image(image):
    row = image.size[0]
    col = image.size[1]
    #t=top r=right b=bottom l=left
    to = ri = bo = le = 0
    flag = 0
    pixels = image.load()
    #/top edge/

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
    #/bottom edge/

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
    #/left edge/

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

    #/right edge/
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
    img = image.crop(box)
    img = img.resize((5, 5), Image.ANTIALIAS)
    pixels = img.load()
    list = []
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r = pixels[j, i][0]
            g = pixels[j, i][1]
            b = pixels[j, i][2]
            if(((r+g+b)/3)>200):
                list.append(1)
                pixels[j,i] = (255,255,255)
            elif(((r+g+b)/3)<=200):
                list.append(0)
                pixels[j,i] = (0,0,0)

    img.save("image.png", 'PNG')
    return list


def main():
    """Main method. Draw interface"""
    net = neu_net.NeuralNetwork()
    try:
        net.W1 = read_list("Weights\W1.w")
        net.W2 = read_list("Weights\W2.w")
    except:
        net.variable_initialization()
        save_list(net.W1, "Weights\W1.w")
        save_list(net.W2, "Weights\W2.w")
    list1 = read_list("Images\.imgs5x5")
    global screen
    pygame.init()
    screen = pygame.display.set_mode((710, 550))
    pygame.display.set_caption("Handwriting recognition")

    background = pygame.Surface((350, 350))
    background.fill((255, 255, 255))
    background2 = pygame.Surface((350, 350))
    background2.fill((255, 255, 255))
    screen.blit(background2, (360, 0))
    pygame.draw.rect(screen, (255, 255, 255), (0, 360, 710, 90))
    pygame.draw.rect(screen, (255, 255, 255), (0, 460, 710, 80))
    conFont = pygame.font.SysFont("Verdana", 14)
    screen.blit(conFont.render("Controles: T\Entrenar A\Predecir C\Limpiar Pantalla Click Derecho\Dibujar Click Izquierdo\Borrar", 1, (0, 0, 0)), (4, 485))

    clock = pygame.time.Clock()
    keepGoing = True
    lineStart = (0, 0)
    drawColor = (0, 0, 0)
    lineWidth = 22
    pygame.display.update()

    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEMOTION:
                lineEnd = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    pygame.draw.circle(background, drawColor, lineStart, lineWidth, 0)
                if pygame.mouse.get_pressed() == (0, 0, 1):
                    pygame.draw.circle(background, (255, 255, 255), lineStart, lineWidth, 0)

                lineStart = lineEnd
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    data = pygame.image.tostring(background, 'RGB')
                    img = Image.fromstring('RGB', (350, 350), data)
                    list = Process_image(img)
                    net.feed_forward(list, False)
                    background2 = pygame.image.load("image.png").convert()
                    background2 = pygame.transform.scale(background2, (350, 350))
                    screen.blit(background2, (360, 0))
                    r, p = net.calculate_results()
                    #myFont = pygame.font.SysFont("Verdana", 24)
                    pygame.draw.rect(screen, (255, 255, 255), (0, 360, 710, 90))
                    myFont = pygame.font.SysFont("Verdana", 24)
                    screen.blit(myFont.render("Letra: %s" % r, 1, (0, 0, 0)), (290, 380))
                    screen.blit(myFont.render("Accuracy: %s" % str(round(p, 4))+"%", 1, (0, 0, 0)), (200, 410))
                if event.key == pygame.K_c:
                    background = pygame.Surface((350, 350))
                    background.fill((255, 255, 255))
                    pygame.draw.rect(screen, (255, 255, 255), (0, 360, 710, 90))
                    background2.fill((255, 255, 255))
                    screen.blit(background2, (360, 0))
                if event.key == pygame.K_t:
                    for iteration in range(0, 1000):
                        for i in range(len(list1)):
                            net.outputs[i] = 1
                            print "Image training: %s" %net.results[i]
                            for j in range(len(list1[i])):
                                net.feed_forward(list1[i][j], True)
                            net.outputs[i] = 0
                        #print "Iteration #%s complete..." %iteration
                    #print "Training done."
                    save_list(net.W1, "Weights\W1.w")
                    save_list(net.W2, "Weights\W2.w")
                if event.key == pygame.K_p:
                    read_5x5_images()
        screen.blit(background, (0, 0))
        pygame.display.flip()


def crop_resize(net):
    #print "Plis w8 loading images"
    all_images =[]
    for x in range(1, 37):
        list_images =[]
        path = "C:\Users\Pablo\Downloads\EnglishHnd\English\Hnd\Img\Sample0"
        path += str(x)
        files = glob.glob(path+"\*.png")
        print x-1
        for file in files:
            img = Image.open(file.title())
            img = Process_image(img)
            list_images.append(img)
        all_images.append(list_images[:])
    #print "All images: " + str(all_images)
    save_list(all_images, "Images\.imgs5x5")
    #print "Loading images complete"




def read_5x5_images():
    path = "C:\Users\Pablo\Pictures\Training set 5x5"
    files = glob.glob(path+"\*.png")
    list_images = []
    for file in files:
        img = Image.open(file.title())
        pixels = img.load()
        list = []
        for i in range(img.size[0]):    # for every pixel:
            for j in range(img.size[1]):
                r = pixels[j, i][0]
                g = pixels[j, i][1]
                b = pixels[j, i][2]
                if(((r+g+b)/3)>200):
                    list.append(1)
                    pixels[j,i] = (255,255,255)
                elif(((r+g+b)/3)<=200):
                    list.append(0)
                    pixels[j,i] = (0,0,0)
        img.save("image.png", 'PNG')
        list_images.append([list])
    save_list(list_images, "Images\.imgs5x5")




def save_list(itemlist, outfile):
    with open(outfile, 'w') as f:
        pck.dump(itemlist, f)

def read_list(infile):
    with open(infile, 'r') as f:
        item_list = pck.load(f)
    return item_list




