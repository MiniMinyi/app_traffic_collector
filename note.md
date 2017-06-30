### create avd instance througn cmd

use android avd

```
echo no | android create avd --force --name testAVD --abi google_apis/x86 -p avds/testAVD -t android-25 --abi google_apis/x86
```

use avdmanager

```
echo no | avdmanager create avd --force --name testAVD --abi google_apis/x86  --package 'system-images;android-25;google_apis;x86' -p avds/testAVD -d 10 
```

list devices

```
avdmanager list devices
```

run emulator (if Library not found occur)

```
cd $(dirname $(which emulator)) && ./emulator -avd testAVD -gpu host -skindir ${HOME}/Library/Android/sdk/skins -skin nexus_6p -no-boot-anim
```

list available android targets

` android list targets`

delete AVD

`android delete avd`

start emulator

```
# then the emulator will be emulator-5555
emulator -avd testAVD -port 5555
# list available AVDs
emulator -list-avds
```

droidbot

```
optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE_SERIAL      The serial number of target device (use `adb devices` to find)
  -a APK_PATH           The file path to target APK
  -o OUTPUT_DIR         directory of output
  -policy INPUT_POLICY  Policy to use for test input generation. Default: dfs.
                        Supported policies:
                          "random" -- Generate random input events.
                          "bfs" -- Explore UI using a breadth-first strategy.
                          "dfs" -- Explore UI using a depth-first strategy.
  -no_shuffle           Explore the UI without view shuffling.
  -script SCRIPT_PATH   Use a script to customize input for certain states.
  -count COUNT          Number of events to generate in total. Default: 1000
  -interval INTERVAL    Interval in seconds between each two events. Default: 1
  -timeout TIMEOUT      Timeout in seconds, -1 means unlimited. Default: -1
  -q                    Run in quiet mode (dump warning messages only).
  -install_app          Don't uninstall the app after testing.
  -use_hierarchy_viewer
                        Force use Hierarchy Viewer to dump UI states instead of UI Automator.
  -use_method_profiling PROFILING_METHOD
                        Record method trace for each event. can be "full" or a sampling rate.
  -grant_perm           Grant all permissions while installing. Useful for Android 6.0+.
  -use_with_droidbox    Use DroidBot with DroidBox. Need to run on a DroidBox emulator.
```

droidbot command

```
droidbot -s 84B7N16531001384 -a /Users/liumy/Desktop/CMU-Project/apks/test/com.yelp.android.apk -script /Users/liumy/Desktop/CMU-Project/apks/test/facebook_login_script.json -o /Users/liumy/Desktop/CMU-Project/apks/test/yelp_output -no_textview -grant_perm
```



install app - use adb

useful command

```
# list all devices
adb devices
# install app
adb -s [emulator name] install [apk file]
```

install droidbot

#### Yelp

**continue with facebook button**

resource id: fb_sign_up_button

class: android.widget.Button

text: CONTINUE WITH FACEBOOK

**facebook login page**

username:

login_username

EditText

password:

login_password

EditText

login_button:

login_login

Button

#### TripAdvisor

**continue with facebook button**

Text: Facebook

rid: facebook_sign_in_button

class: Button

**facebook login page** same with yelp

**Uber**

**navigate to social account**



**navigate to login with facebook account**

class: LinearLayout

content-desc: Sign on using Facebook

class: TextView

text: Facebook

### Work need to do

Stage 1:

1. create emulator if no avd available.
2. start emulator
3. install apk to the emulator
4. run monkey and droidbot.

Stage 2:

1. scale to 10000+ apps.
2. scheduler.
3. local json.



### Useful command

find files in all directories

`find [path] -name "*.apk"`

### scale up to 4w apps



