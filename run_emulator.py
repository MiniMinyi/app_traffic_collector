import os
import subprocess
import time

def createAVD(avdName, outputPath, device, abi, package):
	outputName = os.path.join(outputPath,avdName)
	command = "echo no | avdmanager create avd --force --name "+avdName\
		+" --abi "+abi+"  --package "+package+" -p "+outputName+" -d "+device
	print "EXEC: "+command
	if subprocess.call(command, shell=True) == 0:
		print "create "+avdName +" SUCCESS"

def runEmulator(avdName, port, skin):
	command = "cd $(dirname $(which emulator)) && ./emulator -no-boot-anim -avd "+avdName+\
		" -gpu host -port "+str(port)+" -skindir ${HOME}/Library/Android/sdk/skins -skin "+skin
	print "EXEC: "+command
	child = subprocess.Popen(command, shell=True)

def checkBootStatus(emulatorName):
	command = "adb -s "+emulatorName+" shell getprop init.svc.bootanim"
	# if boot animation has stopped for 10s, then consider the device fully booted
	for i in range(50):
		try:
			output_bytes = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
			output_text = output_bytes.decode('utf-8').strip('\n')
			if output_text == 'stopped':
				print 'INFO: '+emulatorName+' has booted'
				return True
			time.sleep(1)
		except Exception, e:
			time.sleep(1)
	return False

def runDroidbot(apkPath, outputDir, emulator, policy, timeout, script = ''):
	command = 'droidbot -d '+emulator+' -a '+apkPath+\
		' -policy '+policy+' -o '+outputDir+\
		' -timeout '+str(timeout)+' -grant_perm -no_textview'
	if script:
		command += ' -script '+script
	if checkBootStatus(emulator):
		print "EXEC: "+command
		print "Droidbot exit code: ", subprocess.call(command, shell=True)

def runAPKs(apkDir, outputDir, emulator, policy, timeout, script):
	if not os.path.isdir(outputDir):
		os.mkdir(outputDir)
	for f in os.listdir(apkDir):
		if f.endswith('.apk'):
			apkOutDir = os.path.join(outputDir, f[:-4])
			apkPath = os.path.join(apkDir, f)
			runDroidbot(apkPath, apkOutDir, emulator, policy, timeout, script)

def main():
	"""
	the main function
	"""
	# createAVD(avdName='testAVD',outputPath='avds',device="'Nexus 6'", abi='google_apis/x86',package="'system-images;android-25;google_apis;x86'")
	# It's better that port is even number start from 5554
	# runEmulator('testAVD', port=5554, skin='nexus_6p')
	# emulatorName = 'emulator-5554'
	emulatorName = '84B7N16531001384'
	apk = '/Users/liumy/Desktop/CMU-Project/apks/sampledapks/com.yelp.android.apk'
	outputDir = '/Users/liumy/Desktop/CMU-Project/droidbot_output'
	apksDir = '/Users/liumy/Desktop/CMU-Project/apks/download'
	scriptPath = '/Users/liumy/Desktop/CMU-Project/apks/test/facebook_login_script.json'
	runAPKs(apksDir,outputDir=outputDir, emulator=emulatorName, policy='dfs', timeout=120, script=scriptPath)

	# runDroidbot(apkPath=apk, outputDir=outputDir, emulator=emulatorName, policy='dfs', timeout=120, script=scriptPath)

if __name__ == "__main__":
	main()