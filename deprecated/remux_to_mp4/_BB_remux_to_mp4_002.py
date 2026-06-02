'''
Script Name: Remux MP4
Script Version: 1.0
Flame Version: 2024
Modified from script by: Bob Maple
Written by: Bryan Bayley
Creation Date: 2023.07.18
Update Date: 2023.05.18

Notes:
- Using any Movie Preset that has "MP4_H264_" will trigger this script.
- After Export, the script will trigger a process that uses ffmpeg to remux the .mov to .mp4.
- This is a remux, not just renaming the file extension.
- AAC audio must be used to avoid sync issues.
'''

def pre_export_asset(info, userData, *args, **kwargs):
	# Save the resolved (tokens expanded) name of the file that was exported
	# so we can use it later in post_export_sequence which doesn't otherwise
	# get this information
	userData['export_file'] = info['resolvedPath']

def pre_export(info, userData, *args, **kwargs):
	import os
	# Save the export preset name used so we can look at it later
	# in post_export_sequence which doesn't otherwise get this information
	userData['export_preset'] = os.path.basename( info['presetPath'] )

def post_export_sequence(info, userData, *args, **kwargs):
	# Configure a list of preset names to intercept, can use simple * wildcards
	# (and ? for single characters)
	remux_presets = ['MP4_H264*']

	import fnmatch, os, subprocess, time

	for cur_preset in remux_presets:
		if( fnmatch.fnmatch( userData['export_preset'], cur_preset ) == True ):
			remux_source = os.path.join( info['destinationPath'], userData['export_file'] )
			remux_dest   = os.path.join( info['destinationPath'], os.path.splitext( userData['export_file'] )[0] + ".mp4" )

			ffmpeg_cmd = ['/usr/local/bin/ffmpeg', '-y', '-i', remux_source, '-codec:v', 'copy', '-codec:a', 'aac', '-ab', '320k', remux_dest]
			subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

		# Remove the source file if the destination file got created and isn't empty
		if( os.path.isfile(remux_dest) ):
			if( os.path.getsize(remux_dest) > 0 ):
				os.remove( remux_source )
				print("======= MP4 created successfully and MOV was deleted. =======")
			else:
				print("======= MP4 REMUX DID NOT COMPLETE =======")