import pyfiglet


def showLogo(type: str = 'local'):
    figlet_text = ''
    color_text = ''
    if type == 'server':
        figlet_text = pyfiglet.Figlet()
        color_text = figlet_text.renderText('coursePost')
    else:
        figlet_text = pyfiglet.Figlet(font='Soft')
        color_text = figlet_text.renderText('coursePost')
    print(color_text)
