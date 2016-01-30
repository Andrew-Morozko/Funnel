import Handlers
import Settings
import Pipers


def main():
    VK = Handlers.VK(Settings.VK_token)
    Telegram = Handlers.Telegram(Settings.Telegram_token)
    Pipers.autopiper(VK, Telegram)
    Pipers.autopiper(Telegram, VK)


if __name__ == '__main__':
    main()
