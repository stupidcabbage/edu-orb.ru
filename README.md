
# Telegram-bot <b>Дневник Оренбурга
</b>

## <b>Команды бота</b>

* <code>/start</code> - Старт бота (Авторизация / Главное меню)<br>
* <code>/help</code> - Справка<br>
* <code>/diary <i>(Дата по необходимости в формате DD.MM.YYYY)</i></code> - Домашнее задание<br>
* <code>/schedule <i>(Дата по необходимости в формате DD.MM.YYYY)</i></code> - Расписание<br>
* <code>/marks</code> - Получить выписку оценку


## Запуск 
#### 1. Настройка переменных окружения
Скопирутйте <code>.env_example</code> в <code>.env</code> и отредактируйте переменные окружения соответствующими данными.

```
cp .env.example .env
```

#### 2. Установка зависимостей
Для управления зависимостями используется [poetry](https://python-poetry.org/), требуется Python 3.11<br>

```
poetry install
```

#### 3. Установка Chrome + ChromeDriver 
Для работы авторизации через гос.услуги используется [selenium](https://www.selenium.dev/), а именно Chrome + [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)

Чтобы поставить Chrome необходимо получить DEB file, используя команду wget<br>

```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

Теперь можно установить Chrome из DEB файла, используя [dpkg]<br>

```
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

Теперь можно переходить к установке ChromeDriver

Проверяем версию вашего Chrome<br>
```
google-chrome --version

> Google Chrome 119.0.6045.105
```

Переходим на сайт [ChromeDriver](https://chromedriver.chromium.org/downloads/) и устанавливаем такую же стабильную версию, используя wget<br>

```
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chromedriver-linux64.zip
```

Распакуйте архив<br>

```
unzip chromedriver-linux64.zip
```
<br>
Затем введите команды ниже<br>

```
sudo mv chromedriver-linux64 /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```

Chrome и ChromeDriver установлен!<br>
#### 4. Теперь создайте папку для временных файлов<br>

```mkdir diary/temp```<br>

Поздравляю, вы можете запускать бота.
```poetry run python3 -m diary```

