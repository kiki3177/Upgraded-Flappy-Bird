import pygame


class Button(object):
    """
    Define the Button class which represents the general button that can be selected and clicked by the user.
    """

    # initialize the default Button object
    def __init__(self, filename, x=None, y=None, **kwargs):
        self.surface = pygame.image.load('assets/' + filename + '.png') # the surface of the button, which is an image
                                                                        # loaded from external files
        self.surface = pygame.transform.scale(self.surface, (200, 50)) # scale the button image into suitable size

        self.WIDTH = self.surface.get_width()       # get the width of the button
        self.HEIGHT = self.surface.get_height()     # get the height of the button

        # set the general x coordinate of the button in the frame
        if 'centered_x' in kwargs and kwargs['centered_x']:
            self.x = display_width // 2 - self.WIDTH // 2
        else:
            self.x = x

        # set the general y coordinate of the button in the frame
        if 'centered_y' in kwargs and kwargs['centered_y']:
            self.y = display_height // 2 - self.HEIGHT // 2
        else:
            self.y = y

    # display method of the class itself
    def display(self):
        screen.blit(self.surface, (self.x, self.y)) # show on the screen according to the x, y coordinates

    # check if the user clicks the button
    def check_click(self, position):
        # check if the mouse is in the width range of the button
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        # check if the mouse is in the height range of the button
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT

        # if the mouse indeed is in the button area
        if x_match and y_match:
            return True
        else:
            return False

class Bird(object):
    """
    Define the Bird class which inherits the general Object superclass.
    """

    def __init__(self):
        """
        Initialize the Bird object calling the initialize() function.
        """
        self.initialize()

    def initialize(self):
        """
        Define the initialization of the Bird class, since the Bird maybe initialized again
        after events such as death or user backing to the main page, thus is separated here.
        """
        self.birdRect = pygame.Rect(65, 50, 50, 50)  # the square boundingbox of the bird
        # load the image assets of the Bird's status, when 1.png and 2.png represent the flying states of the Bird,
        # and the dead.png shows the dead outlook of the Bird which is used when the Bird is dead
        self.birdStatus = [pygame.image.load("assets/1.png"),
                           pygame.image.load("assets/2.png"),
                           pygame.image.load("assets/dead.png")]
        self.status = 0  # default situation of the Bird's flying state
        self.birdX = 120  # the X coordinate of the Bird, which is its speed to the right
        self.birdY = 350  # the Y coordinate of the Bird, which is the altitude up and down
        self.jump = False  # default situation of the Bird's jumping state, which is False
        self.jumpSpeed = 10  # height of jump
        self.gravity = 5  # gravity
        self.dead = False  # default situation of the Bird's death state, which is False

    def birdupdate(self):
        """
        Update the Bird object according to the states of itself.
        """
        if self.jump:
            # the Bird jumps
            self.jumpSpeed -= 1  # the speed of the Bird decreases, rising up more and more slowly
            self.birdY -= self.jumpSpeed  # the Y coordinate of the Bird decreases, the Bird rises up
            if self.birdY > 620:
                self.birdY = 620
        else:
            # the Bird falls
            self.gravity += 0.2  # the gravity increases, falls down faster and faster
            self.birdY += self.gravity  # the Y coordinate of the Bird increases, the Bird falls down
            if self.birdY > 620:
                self.birdY = 620
        self.birdRect[1] = self.birdY  # change the Y coordinate

class Pipeline(object):
    """
    Define the Pipeline class which inherits the general Object superclass.
    """

    def __init__(self):
        """
        Initialize the Pipeline object calling the initialize() function.
        """
        self.initialize()

    def initialize(self):
        """
        Define the initialization of the Pipeline class, since the Pipeline maybe initialized again
        after events such as death or user backing to the main page, thus is separated here.
        """
        self.wallX = 400  # the X coordinate of the Pipeline
        self.pineUp = pygame.image.load("assets/top.png")
        self.pineDown = pygame.image.load("assets/bottom.png")

    def updatepipeline(self):
        """
        Define the rules of movements of the Pipeline object.
        """
        self.wallX -= 5  # the X coordinate of the Pipeline decreases, that is, the Pipeline moves to the left
        # when the Pipeline reaches a certain position, i.e. the Bird flies over the Pipeline,
        # the score will increase by 1 and the Pipeline resets
        if self.wallX < -80:
            global score
            score += 1
            self.wallX = 400

def start_screen():
    background = pygame.image.load("assets/background.png")  # loading the background image
    screen.blit(background, (0, 0))
    game_title = font.render('Starting Screen', True, (255, 255, 255))
    screen.blit(game_title, (display_width // 2 - game_title.get_width() // 2, 150))

    play_button = Button('SG', None, 350, centered_x=True)
    leaderboard_button = Button('LB', None, 400, centered_x=True)
    exit_button = Button('QG', None, 450, centered_x=True)

    play_button.display()
    leaderboard_button.display()
    exit_button.display()
    pygame.display.update()

    while True:
        if play_button.check_click(pygame.mouse.get_pos()):
            play_button = Button('SG', None, 350, centered_x=True)
        else:
            play_button = Button('SGS', None, 350, centered_x=True)

        if leaderboard_button.check_click(pygame.mouse.get_pos()):
            leaderboard_button = Button('LB', None, 400, centered_x=True)
        else:
            leaderboard_button = Button('LBS', None, 400, centered_x=True)

        if exit_button.check_click(pygame.mouse.get_pos()):
            exit_button = Button('QG', None, 450, centered_x=True)
        else:
            exit_button = Button('QGS', None, 450, centered_x=True)

        play_button.display()
        leaderboard_button.display()
        exit_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # raise SystemExit

        if pygame.mouse.get_pressed()[0]:
            if play_button.check_click(pygame.mouse.get_pos()):
                start_game()
                break
            if leaderboard_button.check_click(pygame.mouse.get_pos()):
                leader_board()
                break
            if exit_button.check_click(pygame.mouse.get_pos()):
                with open('data.txt', 'w') as f:
                    for line in leaderboard:
                        f.write(str(line))
                        f.write('\n')
                raise SystemExit
                break

def leader_board():
    """
    Method which shows the leader board page.
    """
    background = pygame.image.load("assets/background.png")  # loading the background image
    screen.blit(background, (0, 0)) # fill the screen using the given image

    # count is used to show the place of the scores, from 1-0
    count = 0
    # print every line of the score with places
    for line in leaderboard:
        # keeps the counter counting
        count += 1
        # show the line of the score results with different y coordinates
        font_1 = pygame.font.Font("Impact.ttf", 40)  # set the font and the size of text
        screen.blit(font_1.render("TOP " + str(count) + " : " + str(line), True, (255, 255, 255)), (100, 50 + count * 40))
        # only shows the first top 9
        if count > 9:
            break

    # render the back button
    exit_button = Button('Back', None, 540, centered_x=True)
    exit_button.display()
    # update the rendered window
    pygame.display.update()

    # loop forever to refresh and response the user selection
    while True:
        # if the user's mouse focuses on the exit button
        if exit_button.check_click(pygame.mouse.get_pos()):
            exit_button = Button('Back', None, 540, centered_x=True)
        # if the user's mouse loses focus on the exit button
        else:
            exit_button = Button('BackS', None, 540, centered_x=True)

        #show the exit button
        exit_button.display()
        #update the rendered window
        pygame.display.update()

        # capture the pygame events to perform the corresponding behaviours
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        #if the user mouse clicks on the exit button, back to the starting screen
        if pygame.mouse.get_pressed()[0]:
            if exit_button.check_click(pygame.mouse.get_pos()):
                start_screen()
                break

def start_game():
    global score
    score = 0
    Bird.initialize()
    Pipeline.initialize()
    clock = pygame.time.Clock()  # set clock time
    while True:
        clock.tick(60)  # execute 60 times per second
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not Bird.dead:
                Bird.jump = True  # default situation of the Bird's jumping state, which is True
                Bird.gravity = 5  # gravity
                Bird.jumpSpeed = 10  # height of jump

        if checkdead():  # test the Bird's death state
            getresult()  # if the Bird's death state is True which represents the Bird is dead, then show the final scores
        else:
            renderobjects(1)  # render the objects and background on screen
                          # status 1 indicates the normal case, while other indicates game over
            pygame.display.update()  # refresh display

    pygame.quit()

# status 1 indicates the normal case, while other indicates game over
def renderobjects(status):
    background = pygame.image.load("assets/background.png")  # loading the image of background
    """
    renderobjects, is initially used to render the background, bird and the pipeline as well as the score counter on the
    screen. 
    """
    screen.fill((255, 255, 255))  # fill color
    screen.blit(background, (0, 0))  # fill in the background
    # display the Pipeline
    screen.blit(Pipeline.pineUp, (Pipeline.wallX, -300))  # the coordinate of UpPipeline
    screen.blit(Pipeline.pineDown, (Pipeline.wallX, 500))  # the coordinate of DownPipeline
    # only update (move) the pipeline when bird is alive
    if status == 1:
        Pipeline.updatepipeline()  # update the movements of the Pipeline
    # display the Bird
    if Bird.dead:  # the Bird hits the Pipeline
        Bird.status = 2
    elif Bird.jump:  # the Bird jumps
        Bird.status = 1
    screen.blit(Bird.birdStatus[Bird.status], (Bird.birdX, Bird.birdY))  # the coordinate of the position of Bird
    Bird.birdupdate()  # update the movements of the Bird
    # only show scores when game is in progress
    if status == 1:
        screen.blit(font.render('Score:' + str(score), -1, (255, 255, 255)), (100, 50))  # set the color and coordinate position

def checkdead():
    '''
    Define the method to check the death state of the Bird,
    '''
    # the rectangular position of the UpPipeline
    upRect = pygame.Rect(Pipeline.wallX - 40, -300,
                         Pipeline.pineUp.get_width(),
                         Pipeline.pineUp.get_height())

    # the rectangular position of the DownPipeline
    downRect = pygame.Rect(Pipeline.wallX - 40, 500,
                           Pipeline.pineDown.get_width(),
                           Pipeline.pineDown.get_height())
    # test whether the Bird hits the UpPipeline or the DownPipeline
    if upRect.colliderect(Bird.birdRect) or downRect.colliderect(Bird.birdRect):
        Bird.dead = True
        return True
    # test whether the Bird flies beyond the boundaries
    if not 0 < Bird.birdRect[1] < height:
        Bird.birdY = height - 20
        Bird.dead = True
        return True
    else:
        return False

def getresult():
    '''
    Show the final result when game over
    '''
    while True:
        clock = pygame.time.Clock()  # set clock time
        clock.tick(30)  # execute 60 times per second
        renderobjects(2)
        final_text1 = "Game Over"
        final_text2 = "Your final score is:  " + str(score)
        ft1_font = pygame.font.Font("Impact.ttf", 50)  # set the font and the size for the first line of text
        ft2_font = pygame.font.Font("Impact.ttf", 30)  # set the font and the size for the second line of text
        ft1_surf = ft1_font.render(final_text1, 1, (242, 3, 36))  # set the color for the first line of text
        ft2_surf = ft2_font.render(final_text2, 1, (253, 177, 6))  # set the color for the second line of text
        screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # set the display position of the first line of text
        screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 200])  # set the display position of the second line of text
        exit_button = Button('Back', None, 400, centered_x=True)
        exit_button.display()
        if exit_button.check_click(pygame.mouse.get_pos()):
            exit_button = Button('Back', None, 400, centered_x=True)
        else:
            exit_button = Button('BackS', None, 400, centered_x=True)

        exit_button.display()
        pygame.display.flip()  # update the entire Surface object to be displayed on the screen

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # raise SystemExit

        if pygame.mouse.get_pressed()[0]:
            if exit_button.check_click(pygame.mouse.get_pos()):
                leaderboard.append(score)
                leaderboard.sort()
                leaderboard.reverse()
                start_screen()

if __name__ == '__main__':
    """
    Main program
    """
    leaderboard = []
    score = 0

    with open('data.txt', 'r') as f:
        for line in f:
            leaderboard.append(int(line.strip('\n')))
    print(leaderboard)
    f.close()

    Pipeline = Pipeline()  # instantiate the Pipeline class
    Bird = Bird()  # instantiate the Bird class
    pygame.init()  # initialize pygame
    pygame.font.init()  # initialize the font
    font = pygame.font.Font("Impact.ttf", 50)  # set the font and the size of text
    size = width, height = 400, 650  # set the window
    display_width = 400
    display_height = 650
    screen = pygame.display.set_mode(size)  # display the window
    start_screen()  # enter the start_screen() method



