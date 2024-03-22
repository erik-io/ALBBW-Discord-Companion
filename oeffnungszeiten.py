def oeffnungszeiten_info():
        return (f'# Cafeteria\n'
                f'__**Öffnungszeiten:**__\n'
                f'```Montag - Freitag        08:30 Uhr - 15:00 Uhr\n'
                f'Sonderöffnungszeiten    08:30 Uhr - 10.30 Uhr\n'
                f'Mobile Cafeteria        08:30 Uhr - 11:00 Uhr```\n')

def kaffee_info():
        return (f'__**Kaffeespezialitäten:**__\n'
            f'```Milchkaffee                      1,70 €\n'
            f'Heiße Schokolade                 1,70 €\n'
            f'Cappuccino                       1,50 €\n'
            f'Schokoccino                      1,70 €\n'
            f'Latte Macciato                   1,70 €\n'
            f'Espresso                         1,00 €\n'
            f'Doppelter Espresso               1,70 €\n'
            f'Espresso Macchiato               1,30 €\n'
            f'Café Créme                       1,45 €```\n')
def cafeteria_info():
    return (oeffnungszeiten_info() +
            f'\n' +
            kaffee_info() +
            f'\n'
            f'__**Getränke:**__\n'
            f'```Eistee Orange, 0,5l              1,20 €\n'
            f'Eistee Himbeere, 0,5l            1,20 €\n'
            f'Eistee Apfel, 0,5l               1,20 €\n'
            f'Eistee Multivitamin, 0,5l        1,20 €\n'
            f'H-Drink Vanille, 0,5l            1,30 €\n'
            f'H-Drink Erdbeere, 0,5l           1,30 €\n'
            f'H-Drink Schoko, 0,5l             1,30 €\n'
            f'H-Drink Banane, 0,5l             1,30 €\n'
            f'Capri Sun, 0,2l                  0,65 €\n'
            f'Mineralwasser 0,75l              1,15 €\n'
            f'Coca Cola, 0,33l                 1,40 €\n'
            f'Sprite, 0,33l                    1,40 €\n'
            f'Fanta, 0,5l                      1,70 €\n'
            f'Kaffee klein, 0,2 l              1,20 €\n'
            f'Kaffee groß, 0,3 l               1,65 €```\n'
            f'\n'
            f'__**Süßwaren und Snacks:**__\n'
            f'```Cookie, 100 g hell und dunkel    1,80 €\n'
            f'Snickers, 50 g                   0,90 €\n'
            f'Twix, 50 g                       0,90 €\n'
            f'Mars, 51 g                       0,90 €\n'
            f'Leibniz Minis Choco, 125 g       2,10 €\n'
            f'Leibniz Choco 125 g              2,10 €\n'
            f'Pringles, 40 g                   1,40 €\n'
            f'Mentos Frucht, 38 g              0,90 €\n'
            f'Duplo, 18,2 g                    0,40 €\n'
            f'Kinder Riegel, 21 g              0,40 €\n'
            f'Brötchen, Sandwich               1,90 €\n'
            f'Salat, groß                      3,20 €\n'
            f'Salat, klein                     1,70 €\n```')