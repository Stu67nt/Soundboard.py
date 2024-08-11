import pygame
import os
import threading
import time

"""
TODO:
|Make colour states depending on button interaction|  I couldn't get active to work if anyone can figure out how to do so please help.
  Each button will change its shade slightly depending on how the user is interacting with it.
  There will be 3 states:
    Default (No interaction  with button.)
    Hovering (Mouse is hovering over the button. Ends when users mouse has either moved off button or clicked button.)
    Active (User has clicked the button. Ends when the button's process has finished)
  """

options_flag = False
is_clicked = 0
accept_input = True


# Clears console
def cls():
  os.system('cls' if os.name == 'nt' else 'clear')  # Some guy on Stack Overflow said this was a good way of doing it.


def colour_darkener(hexcode: str):
  hexadecimal = hexcode.replace("#", "", 1)
  digits = []
  
  for char in hexadecimal:
    digits.append(char)
  
  red = int((digits[0] + digits[1]), 16) - 20
  green = int((digits[2] + digits[3]), 16) - 20
  blue = int((digits[4] + digits[5]), 16) - 20
  
  if red < 0:
    red = 0
  if green < 0:
    green = 0
  if blue < 0:
    blue = 0
  
  newhex = ("#" + (hex(red).replace("0x", "", 1)) + (hex(green).replace("0x", "", 1)) +
            (hex(blue).replace("0x", "", 1)))
  while len(newhex) < 7:
    newhex = newhex + "0"
  return newhex


def replace_line(file_name: str, line_num: int, text: str):
  with open(file_name, 'r') as file:
    settings_data = file.readlines()
    settings_data[line_num - 1] = text
    file.close()
  with open(file_name, 'w') as file:
    file.writelines(settings_data)
    file.close()


def find_setting_line(file_name: str, text: str):
  counter = 0
  with open(file_name, 'r') as file:
    for line in file:
      if line.find(text) != -1:
        counter = counter + 1
        file.close()
        return counter
      counter = counter + 1
    return -1


def is_hexadecimal(value: str):
  try:
    int(value, 16)
    return True
  except ValueError:
    return False


def validate_hexcode(input: str):
  if len(input) != 7:
    print("The input should be a '#' followed by 6 numbers of letters between 'A' and 'F' such as #A1B2C3.")
    return False
  if input[0] != "#":
    print("The input should be a '#' followed by 6 numbers of letters between 'A' and 'F' such as #A1B2C3.")
    return False
  if not is_hexadecimal(input.replace("#", "", 1)):
    print("The input should be a '#' followed by 6 numbers of letters between 'A' and 'F' such as #A1B2C3.")
    return False
  else:
    return True


# Used for making the settings menu and validating input into the settings menu
def handle_options():
  global accept_input
  length = ""
  height = ""
  
  while True:
    print("You have entered options. What would you like to do?\n"
          "1. Set/Change File directory\n"
          "2. Change window resolution\n"
          "3. Change button name\n"
          "4. Change file set to button\n"
          "5. Change button colours\n"
          "6. Change window name\n"
          "7. Exit Options")
    command = input("Enter a number which is associated with the corresponding option: ")
    
    if command == '1':
      text = input("Enter folder location: ")
      
      replace_line("Settings", 2, "Audio File directory:" + text + "\n")
      
      input("Action Complete. Press enter to return to the settings menu. ")
      cls()
    
    elif command == '2':
      while not length.isdigit() and not height.isdigit():
        length = input("Enter how long you want the window to be: ")
        height = input("Enter how tall you want the window to be.")
      
      replace_line("Settings", 3, "Window Resolution:" + length + ", " + height + "\n")
      
      input("Action Complete. Press enter to return to the settings menu. ")
      cls()
    
    elif command == "3":
      to_change = input("Enter the button you want to change: ")
      change_to = input("Enter what you want to change it to: ")
      
      line_num = find_setting_line("Settings", to_change + " Name:")
      
      while line_num == -1:
        print("Incorrect Button Name. "
              "Top Left button is Button 1. "
              "Top right button is Button 5. "
              "Bottom left is Button 16")
        
        to_change = input("Enter the button you want to change: ")
        line_num = find_setting_line("Settings", to_change + " Name:")
      
      replace_line("Settings", line_num, to_change + " Name:" + change_to + "\n")
      input("Action Complete. Press enter to return to the settings menu. ")
      cls()
    
    elif command == "4":
      to_change = input("Enter the button you want to change the file path of: ")
      change_to = input("Enter the file name you want to change it to (include the file extension (.mp3, .wav)): ")
      line_num = find_setting_line("Settings", to_change + " File:")
      
      while line_num == -1:
        print(
          "Incorrect Button Name. "
          "Top Left button is Button 1. "
          "Top right button is Button 5. "
          "Bottom left is Button 16")
        
        to_change = input("Enter the button you want to change: ")
        line_num = find_setting_line("Settings", to_change + " File:")
      
      replace_line("Settings", line_num, to_change + " File:" + change_to + "\n")
      input("Action Complete. Press enter to return to the settings menu. ")
      cls()
    
    elif command == "5":
      valid = False
      
      to_change = input("Enter the button you want to change the colour of: ")
      
      line_num = find_setting_line("Settings", to_change + " Colour:")
      while line_num == -1:
        print("Incorrect Button Name. "
              "Top Left button is Button 1. "
              "Top right button is Button 5. "
              "Bottom left is Button 16. ")
        to_change = input("Enter the button you want to change: ")
        line_num = find_setting_line("Settings", to_change + " Colour:")
      
      while not valid:
        change_to = input("Enter the hexcode of what you want to change it to (eg: #FFFFFF is white): ")
        valid = validate_hexcode(change_to)
      
      replace_line("Settings", line_num, to_change + " Colour:" + change_to + "\n")
      
      input("Action Complete. Press enter to return to the settings menu. ")
      cls()
    
    elif command == "6":
      text = input("Enter new window name: ")
      
      replace_line("Settings", 1, "Window:" + text + "\n")
      
      input("Action Complete. Press enter to return to the settings menu. ")
      cls()
    
    elif command == '7':
      accept_input = True
      
      cls()
      print("You have left the settings menu please return to the main window.")
      
      break
    
    else:
      print("Invalid option. Please try again.")


# Plays the audio file that is requested or sends request to change the folder location.
def audio_player(selection: str):
  # Initialize the mixer module
  pygame.mixer.init()
  
  try:
    # Opens file where the file path to folder with audio file is located.
    directory = retrieve_setting(2, "Audio File Directory:")
    filepath = directory + selection  # Mushes the audio file name and file path into one variable.
    
    pygame.mixer.music.load(filepath)  # Loads the audio file. Errors occur here if the user has done something wrong.
    pygame.mixer.music.play()  # Plays audio file
    while pygame.mixer.music.get_busy():  # Ensures the audio file keeps playing until it is finished.
      for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
          break
        elif event.type == pygame.QUIT:
          pygame.quit()
        else:
          continue
  
  except pygame.error as err:  # Catches any errors normally due to user misuse
    if str(err) != 'mixer not initialized':
      
      file = open("LatestCrashLog.txt", "w")
      file.write("Something went wrong trying to play this file. \n"
                 "Check the set file location contains the file or file your trying to play is in the correct format.\n"
                 "Should look something like C:\\Users\\tanzi\\PycharmProjects\\Soundboard\\Audio Files\\\n"
                 "Current set directory: " + directory +
                 "\nFile you attempted to play: " + selection
                 )
      file.close()
      print("An error occurred. It could be because Folder Location not being formatted or set correctly. \n"
            "It could also be because the file you are trying to play does not exist or is in the incorrect format.\n"
            "(Accepted ones are .wav and .mp3)\n"
            "Recorded on LatestCrashLog.txt. \n")
      time.sleep(0.4)
    
    elif str(err) == 'mixer not initialized':
      pass
    else:
      print("Idk what went wrong check LatestCrashLog.txt and lmk how it happened.")
      file = open("LatestCrashLog.txt", "w")
      file.write(str(err))


# This function exists aas a way for the program to find what a thing should be assigned to or look like using the
# 'Settings' file.
def retrieve_setting(line_num: int, to_remove: str, file_name='Settings'):
  with open(file_name, 'r') as file:
    settings_data = file.readlines()
    file.close()
    return settings_data[line_num - 1].replace(to_remove, "", 1).rstrip()


# Way too many required inputs for this I could remove some, but I want it to be more freeing.
def audio_button(screen, rx1: (float, int), ry1: (float, int), rx2: (float, int), ry2: (float, int),
                 button_colour: str, button_text: str, font_colour: str, full_file_name: str):
  width = screen.get_width()
  height = screen.get_height()
  x_unit = width / 5
  y_unit = height / 4
  mouse = pygame.mouse.get_pos()
  font = pygame.font.SysFont('comic sans', 28)
  click = pygame.mouse.get_pressed()
  global accept_input
  
  pygame.draw.rect(screen, button_colour, [rx1, ry1, rx2, ry2])
  text = font.render(button_text, True, font_colour)
  screen.blit(text, (rx1 + 10, ry1 + 10))
  
  if rx1 <= mouse[0] < (rx1 + rx2) and ry1 <= mouse[1] < (ry1 + ry2) and accept_input:
    hover_colour = colour_darkener(button_colour)
    pygame.draw.rect(screen, hover_colour, [rx1, ry1, rx2, ry2])
    screen.blit(text, (rx1 + 10, ry1 + 10))
    
    if click[0] == 1:  # Thank you, ChatGPT!
      if full_file_name != '' and full_file_name != ' ':
        audio_player(full_file_name)
      else:
        print("No audio file has been set to this button. Set one.")
        time.sleep(0.2)  # Stops spamming console too fast from holding down as I allow holding down buttons.
  else:
    pass


def function_button(screen, rx1: (float, int), ry1: (float, int), rx2: (float, int), ry2: (float, int),
                    tx1: (float, int), ty1: (float, int)):
  global options_flag
  global is_clicked
  global accept_input
  mouse = pygame.mouse.get_pos()
  font = pygame.font.SysFont('comic sans', 28)
  click = pygame.mouse.get_pressed()
  
  pygame.draw.rect(screen, '#CCCCCC', [rx1, ry1, rx2, ry2])
  text = font.render("Options", True, "#FFFFFF")
  screen.blit(text, (tx1, ty1))
  if click[0] == 1 and is_clicked == 0:
    is_clicked = 1
  
  if rx1 <= mouse[0] < (rx1 + rx2) and ry1 <= mouse[1] < (ry1 + ry2):
    hover_colour = colour_darkener('#CCCCCC')
    pygame.draw.rect(screen, hover_colour, [rx1, ry1, rx2, ry2])
    screen.blit(text, (rx1 + 10, ry1 + 10))
    if is_clicked == 1 and accept_input:
      options_flag = True
      is_clicked = 2
      accept_input = False
  
  if click[0] == 0:
    is_clicked = 0


def main_window():
  global options_flag
  pygame.init()
  default_res = tuple(map(int, retrieve_setting(3, "Window Resolution:").split(', ')))
  screen = pygame.display.set_mode(default_res, pygame.RESIZABLE)
  clock = pygame.time.Clock()
  pygame.display.set_caption(retrieve_setting(1, "Window:"))  # Gives the window a name
  running = True  # Keep this true as it is what tells the program to run the main loop
  font = pygame.font.SysFont('comic sans', 50)
  
  while running:
    width = screen.get_width()
    height = screen.get_height()
    x_unit = width / 5  # These exist as a way of making the buttons easier to place rather than making the coordinates
    y_unit = height / 4  # really long. This allows for a maximum of 20 buttons to be placed. Adjust values if you want more buttons.
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    
    if accept_input:  # Only renders main screen if the settings menu is open which is checked by checking if input is accepted which is only turned off during settings.
      screen.fill("white")  # Wipes everything from the previous frame.
      
      # First row buttons.
      audio_button(screen, 0, 0, x_unit, y_unit, retrieve_setting(6, "Button 1 Colour:"),
                   retrieve_setting(4, "Button 1 Name:"), '#000000', retrieve_setting(5, "Button 1 File:"))
      audio_button(screen, x_unit, 0, x_unit, y_unit, retrieve_setting(9, "Button 2 Colour:"),
                   retrieve_setting(7, "Button 2 Name:"), '#000000', retrieve_setting(8, "Button 2 File:"))
      audio_button(screen, (2 * x_unit), 0, x_unit, y_unit, retrieve_setting(12, "Button 3 Colour:"),
                   retrieve_setting(10, "Button 3 Name:"), '#000000', retrieve_setting(11, "Button 3 File:"))
      audio_button(screen, (3 * x_unit), 0, x_unit, y_unit, retrieve_setting(15, "Button 4 Colour:"),
                   retrieve_setting(13, "Button 4 Name:"), '#000000', retrieve_setting(14, "Button 4 File:"))
      audio_button(screen, (4 * x_unit), 0, x_unit, y_unit, retrieve_setting(18, "Button 5 Colour:"),
                   retrieve_setting(16, "Button 5 Name:"), '#000000', retrieve_setting(17, "Button 5 File:"))
      
      # Second row Buttons
      audio_button(screen, 0, y_unit, x_unit, y_unit, retrieve_setting(21, "Button 6 Colour:"),
                   retrieve_setting(19, "Button 6 Name:"), '#000000', retrieve_setting(20, "Button 6 File:"))
      audio_button(screen, x_unit, y_unit, x_unit, y_unit, retrieve_setting(24, "Button 7 Colour:"),
                   retrieve_setting(22, "Button 7 Name:"), '#000000', retrieve_setting(23, "Button 7 File:"))
      audio_button(screen, (2 * x_unit), y_unit, x_unit, y_unit, retrieve_setting(27, "Button 8 Colour:"),
                   retrieve_setting(25, "Button 8 Name:"), '#000000', retrieve_setting(26, "Button 8 File:"))
      audio_button(screen, (3 * x_unit), y_unit, x_unit, y_unit, retrieve_setting(30, "Button 9 Colour:"),
                   retrieve_setting(28, "Button 9 Name:"), '#000000', retrieve_setting(29, "Button 9 File:"))
      audio_button(screen, (4 * x_unit), y_unit, x_unit, y_unit, retrieve_setting(33, "Button 10 Colour:"),
                   retrieve_setting(31, "Button 10 Name:"), '#000000', retrieve_setting(32, "Button 10 File:"))
      
      # Third row buttons
      audio_button(screen, 0, (2 * y_unit), x_unit, y_unit, retrieve_setting(36, "Button 11 Colour:"),
                   retrieve_setting(34, "Button 11 Name:"), '#000000', retrieve_setting(35, "Button 11 File:"))
      audio_button(screen, x_unit, (2 * y_unit), x_unit, y_unit, retrieve_setting(39, "Button 12 Colour:"),
                   retrieve_setting(37, "Button 12 Name:"), '#000000', retrieve_setting(38, "Button 12 File:"))
      audio_button(screen, (2 * x_unit), (2 * y_unit), x_unit, y_unit, retrieve_setting(42, "Button 13 Colour:"),
                   retrieve_setting(40, "Button 13 Name:"), '#000000', retrieve_setting(41, "Button 13 File:"))
      audio_button(screen, (3 * x_unit), (2 * y_unit), x_unit, y_unit, retrieve_setting(45, "Button 14 Colour:"),
                   retrieve_setting(43, "Button 14 Name:"), '#000000', retrieve_setting(44, "Button 14 File:"))
      audio_button(screen, (4 * x_unit), (2 * y_unit), x_unit, y_unit, retrieve_setting(48, "Button 15 Colour:"),
                   retrieve_setting(46, "Button 15 Name:"), '#000000', retrieve_setting(47, "Button 15 File:"))
      
      # Fourth row buttons
      audio_button(screen, 0, (3 * y_unit), x_unit, y_unit, retrieve_setting(51, "Button 16 Colour:"),
                   retrieve_setting(49, "Button 16 Name:"), '#000000', retrieve_setting(50, "Button 16 File:"))
      audio_button(screen, x_unit, (3 * y_unit), x_unit, y_unit, retrieve_setting(54, "Button 17 Colour:"),
                   retrieve_setting(52, "Button 17 Name:"), '#000000', retrieve_setting(53, "Button 17 File:"))
      audio_button(screen, (2 * x_unit), (3 * y_unit), x_unit, y_unit, retrieve_setting(57, "Button 18 Colour:"),
                   retrieve_setting(55, "Button 18 Name:"), '#000000', retrieve_setting(56, "Button 18 File:"))
      audio_button(screen, (3 * x_unit), (3 * y_unit), x_unit, y_unit, retrieve_setting(60, "Button 19 Colour:"),
                   retrieve_setting(58, "Button 19 Name:"), '#000000', retrieve_setting(59, "Button 19 File:"))
      function_button(screen, (4 * x_unit), (3 * y_unit), x_unit, y_unit, (4 * x_unit) + 10, (3 * y_unit) + 10)
      
      pygame.display.flip()
    
    if not accept_input:
      screen.fill("white")
      text = font.render("Go to the Command Window", True, "black")
      screen.blit(text, (x_unit, y_unit))
      pygame.display.flip()
    
    if options_flag:  # Both the main window and command line are ran to the same time as if the main window isn't doing anything for 5 seconds it crashes.
      cls()
      options_flag = False
      options_thread = threading.Thread(target=handle_options)
      options_thread.start()
    
    clock.tick(30)  # This value changes the max frame rate adjust as needed
  
  pygame.quit()
  raise SystemExit


# Prompts the actual program to run.
try:
  cls()
  main_window()
except pygame.error as err:
  if str(err) == "display Surface quit":  # Exists as a way to prevent an error message opening up when trying to close the program whilst an audio file is playing.
    pass
