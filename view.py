import pygame.font, pygame.event, pygame.draw
from PIL import Image
from Models import neural_network as neu_net
import pickle as pck
import glob
import tkMessageBox

net = neu_net.NeuralNetwork()
bkgnd_draw = pygame.Surface((350, 350))

def Process_image(image):
    row = image.size[0]
    col = image.size[1]



    pixels = image.load()
    new_col = 10000000
    new_col2 = -1
    list_ima =[]
    first_column =False
    white_column= True

    for x in range(col):
        white_column = True
        for y in range(row):
            r = pixels[y, x][0]
            g = pixels[y, x][1]
            b = pixels[y, x][2]
            #Si hay un negro
            if(((r+g+b)/3)<=200)&(first_column == False):
                print "hola", x ,y
                new_col = x
                first_column = True
            if(((r+g+b)/3)<=200)&(white_column == True):
                print "hola", x ,y
                white_column = False
                break
        if (white_column == True)&(first_column == True):
            list_ima.append([new_col, x])
            first_column = False




    print list_ima


    box = define_box(pixels,row, col)

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

def define_box(pixels,row, col):
    to = ri = bo = le = 0
    to = le = 1000000
    flag = 0
    #top edge
    for x in range(row):
        for y in range(col):
            r = pixels[x, y][0]
            g = pixels[x, y][1]
            b = pixels[x, y][2]
            #Si hay un negro
            if(((r+g+b)/3)<=200):

                if x<to:
                    to = x
                if x>=bo:
                    bo = x
                if y<le:
                    le = y
                if y>=ri:
                    ri = y
                break
    box = (to, le, bo, ri)
    print box
    return box




def view_initialization():
    list1 = read_list("Images\.imgs5x5")
    global screen
    pygame.init()
    screen = pygame.display.set_mode((710, 550))
    pygame.display.set_caption("Handwriting recognition")

    bkgnd_draw = pygame.Surface((350, 350))
    bkgnd_draw.fill((255, 255, 255))
    background2 = pygame.Surface((350, 350))
    background2.fill((255, 255, 255))
    screen.blit(background2, (360, 0))
    pygame.draw.rect(screen, (255, 255, 255), (0, 460, 710, 80))
    pygame.draw.rect(screen, (255, 255, 255), (0, 360, 710, 90))
    conFont = pygame.font.SysFont("Verdana", 14)
    screen.blit(conFont.render("Controles: T\Entrenar A\Predecir C\Limpiar Pantalla Click Derecho\Dibujar Click Izquierdo\Borrar", 1, (0, 0, 0)), (4, 485))

    clock = pygame.time.Clock()
    keepGoing = True
    lineStart = (0, 0)
    drawColor = (30, 50, 90)
    lineWidth = 22
    pygame.display.update()


def view_initialization_from_MV(bkgnd_):
    list1 = read_list("Images\.imgs5x5")
    global screen
    pygame.init()
    screen = pygame.display.set_mode((710, 550))
    pygame.display.set_caption("Handwriting recognition")

    bkgnd_draw = pygame.Surface((350, 350))
    bkgnd_draw.fill((255, 255, 255))
    background2 = pygame.Surface((350, 350))
    background2.fill((255, 255, 255))
    screen.blit(background2, (360, 0))
    pygame.draw.rect(screen, (255, 255, 255), (0, 460, 710, 80))
    pygame.draw.rect(screen, (255, 255, 255), (0, 360, 710, 90))
    conFont = pygame.font.SysFont("Verdana", 14)
    screen.blit(conFont.render("Controles: E\Entrenar \nP\Predecir \nC\Limpiar Pantalla Click Derecho\Dibujar Click Izquierdo\Borrar", 1, (0, 0, 0)), (4, 485))

    clock = pygame.time.Clock()

    lineStart = (0, 0)
    drawColor = (30, 50, 90)
    lineWidth = 22
    pygame.display.update()

def main(load_img,image):
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
    pygame.display.set_caption("Reconocimiento de Caracteres")

    bkgnd_draw = pygame.Surface((350, 350))
    bkgnd_draw.fill((255, 255, 255))
    background2 = pygame.Surface((350, 350))
    background2.fill((255, 255, 255))
    screen.blit(background2, (360, 0))
    pygame.draw.rect(screen, (255, 255, 255), (0, 460, 710, 80))
    pygame.draw.rect(screen, (255, 255, 255), (0, 360, 710, 90))
    conFont = pygame.font.SysFont("Verdana", 14)
    screen.blit(conFont.render("Controles: T\Entrenar A\Predecir C\Limpiar Pantalla Click Derecho\Dibujar", 1, (0, 0, 0)), (4, 485))

    clock = pygame.time.Clock()
    keepGoing = True
    lineStart = (0, 0)
    drawColor = (30, 50, 90)
    lineWidth = 22
    pygame.display.update()

    if load_img:
        bkgnd_draw = pygame.image.load(image)
        predict_image(bkgnd_draw, net)
    while keepGoing:
        clock.tick(300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEMOTION:
                lineEnd = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    pygame.draw.circle(bkgnd_draw, drawColor, lineStart, lineWidth, 0)
                if pygame.mouse.get_pressed() == (0, 0, 1):
                    pygame.draw.circle(bkgnd_draw, (255, 255, 255), lineStart, lineWidth, 0)
                lineStart = lineEnd
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    predict_image(bkgnd_draw, net)
                if event.key == pygame.K_c:
                    bkgnd_draw = pygame.Surface((350, 350))
                    bkgnd_draw.fill((255, 255, 255))
                    pygame.draw.rect(screen, (255, 255, 255), (0, 360, 710, 90))
                    background2.fill((255, 255, 255))
                    screen.blit(background2, (360, 0))
                if event.key == pygame.K_t:
                    while net.unbalanced:
                        net.unbalanced = False
                        for i in range(len(list1)):
                            net.outputs[i] = 1
                            for j in range(len(list1[i])):
                                net.feed_forward(list1[i][j], True)
                            net.outputs[i] = 0
                    print "Training done."
                    save_list(net.W1, "Weights\W1.w")
                    save_list(net.W2, "Weights\W2.w")
                if event.key == pygame.K_p:
                    read_5x5_images()
        screen.blit(bkgnd_draw, (0, 0))
        pygame.display.flip()


def crop_resize(net):
    all_images =[]
    for x in range(1, 37):
        list_images =[]
        path = "E:\Users\Lesmed\Downloads\EnglishHnd\English\Hnd\Img\Sample0"
        path += str(x)
        files = glob.glob(path+"\*.png")
        print x-1
        for file in files:
            img = Image.open(file.title())
            img = Process_image(img)
            list_images.append(img)
        all_images.append(list_images[:])
    save_list(all_images, "Images\.imgs5x5")


#Trains.

def read_5x5_images():
    path = "E:\Users\Lesmed\Pictures\Training set 5x5"
    files = glob.glob(path+"\*.png")
    list_images = []
    for file in files:
        img = Image.open(file.title())
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
        list_images.append([list])
    save_list(list_images, "Images\.imgs5x5")




def save_list(itemlist, outfile):
    with open(outfile, 'w') as f:
        pck.dump(itemlist, f)

def read_list(infile):
    with open(infile, 'r') as f:
        item_list = pck.load(f)
    return item_list

def predict_image(bkgnd_draw, net):
    imageData = pygame.image.tostring(bkgnd_draw, 'RGB')
    #print "Data :" , imageData
    img = Image.fromstring('RGB', (350, 350), imageData)
    list = Process_image(img)
    #print list
    net.feed_forward(list, False)
    try:
        view_initialization()
    except:
        pass
    background2 = pygame.image.load("image.png").convert()
    background2 = pygame.transform.scale(background2, (350, 350))
    screen.blit(background2, (360, 0))
    r, p = net.calculate_results()
    #myFont = pygame.font.SysFont("Verdana", 24)
    pygame.draw.rect(screen, (255, 255, 255), (0, 360, 710, 90))
    myFont = pygame.font.SysFont("Verdana", 24)
    screen.blit(myFont.render("Caracter: %s" % r, 1, (0, 0, 0)), (290, 380))
    screen.blit(myFont.render("Precision: %s" % str(round(p, 4))+"%", 1, (0, 0, 0)), (200, 410))
    tkMessageBox.showinfo("Resultados", "Caracter: " + str(r) + " Precision: " + str(p) )













