import mmh3
import base64
import time
import colorama

colorama.init()

def main():
    try:
       with open('favicon.ico', 'rb') as f:
            data = f.read()
            pass
       b64 = base64.encodebytes(data)
       favicon_hash = mmh3.hash(b64)
       print(f'{colorama.Fore.WHITE}[{colorama.Fore.BLUE}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.LIGHTGREEN_EX}Получен Хеш FavIcon') if favicon_hash is not None else print(f'{colorama.Fore.RED}Ошибка генерации')
       print(f'{colorama.Fore.WHITE}[{colorama.Fore.BLUE}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.LIGHTGREEN_EX}Hash{colorama.Fore.RED}: {colorama.Fore.YELLOW}{favicon_hash}{colorama.Fore.RESET}')
    except FileNotFoundError:
           print(f'file not found')

if __name__ == "__main__":
   main()
