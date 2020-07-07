"""Simple script to add thumbnails to mp3 files.

Folder structure:
  Artwork/
  Music/
  AddMusicArtwork.py

This script makes use of the above folder structure.
The Artwork/ and Music/ folders must contain the same number of
PNG and MP3 files respectively.

This script also makes use of various Ubuntu packages.
For more information, see AddingMusicArtwork.md
"""

import logging, os, sys

def validateFolderStructure(artworkFolder, musicFolder, thumbnailsFolder):
  """Validate the folder structure as defined in the header comment.

  Arguments:
    artworkFolder (str): Path to the original artwork folder, unguaranteed
    musicFolder (str): Path to the music folder, unguaranteed
    thumbnailsFolder (str): Path to the thumbnails folder, unguaranteed

  Raises:
    IOError: If any of the arguments are not folders
  """
  # Check folders exist
  if (os.path.isdir(artworkFolder)
    and os.path.isdir(musicFolder)
    and os.path.isdir(thumbnailsFolder)):
    pass
  else:
    logging.critical('Missing artwork, music, or thumbnails folders:\n'
      f'  {artworkFolder}\n  {musicFolder}\n  {thumbnailsFolder}')
    raise IOError

def validateFilePaths(filePathList, fileExtension):
  """Validate the given file paths.

  Check that the file exists. Verify the file has the proper extension.

  Arguments:
    filePathList (list(str)): List of file paths to validate
    fileExtension (str): The file extension, starting with '.'

  Returns:
    list(str): Valid files, excluding the file path
  """
  validFiles = []
  for filePath in filePathList:
    if not os.path.isfile(filePath):
      logging.error(f'Invalid file path: {filePath}')
      continue
    if not filePath.endswith(fileExtension):
      logging.error(f'{filePath} does not have the {fileExtension}')
      continue
    validFiles.append(filePath)
  return validFiles

def convertEquivalents(filePathList, newFileExtension, newFolderPath):
  """Convert file names to the new file extension.

  Arguments:
    filePathList (list(str)): Valid file paths to convert
    newFileExtension (str): The file extension, starting with '.'
    newFolderPath (str): The new folder path

  Returns:
    list(str): Valid file paths
  """
  newFilePaths = []
  for filePath in filePathList:
    _, fileName = os.path.split(filePath)
    splitFileName = fileName.split('.')
    splitFileName[-1] = newFileExtension[1:] # Don't include the .
    newFileName = '.'.join(splitFileName)
    newFilePath = os.path.join(newFolderPath, newFileName)
    if not os.path.isfile(newFilePath):
      logging.error(f'Invalid new file path: {newFilePath}')
      continue
    newFilePaths.append(newFilePath)
  return newFilePaths

def getOriginalPairedFilePaths(artworkFolder, musicFolder):
  """Get the paired original artwork and music file paths.

  Arguments:
    artworkFolder (str): Path to the original artwork folder, guaranteed
    musicFolder (str): Path to the music folder, guaranteed

  Raises:
    IOError: If there is a mismatching number of PNG and MP3 files

  Returns:
    list(str): File paths of valid artwork files
    list(str): File paths of valid music files
  """
  artworkFileNameList = os.listdir(artworkFolder)
  musicFileNameList = os.listdir(musicFolder)
  
  # Check matching number of image and audio files
  if len(artworkFileNameList) != len(musicFileNameList):
    logging.critical('Mismatching number of artwork and music files: '
      f'{len(artworkFileNameList)}, {len(musicFileNameList)}')
    raise IOError

  pairedFileNameList = zip(artworkFileNameList, musicFileNameList)

  actualArtworkFilePathList = []
  actualMusicFilePathList = []

  for pngFileName, mp3FileName in pairedFileNameList:

    if not pngFileName.endswith('.png'):
      logging.error(f'{pngFileName} is not a PNG file')
      continue
    
    if not mp3FileName.endswith('.mp3'):
      logging.error(f'{mp3FileName} is not a MP3 file')
      continue
    
    if pngFileName.split('.')[0] != mp3FileName.split('.')[0]:
      logging.error('File names are not the same:\n'
          f'  {pngFileName}\n  {mp3FileName}')
      continue

    pngFilePath = os.path.join(artworkFolder, pngFileName)
    actualArtworkFilePathList.append(pngFilePath)

    mp3FilePath = os.path.join(musicFolder, mp3FileName)
    actualMusicFilePathList.append(mp3FilePath)

  return actualArtworkFilePathList, actualMusicFilePathList

def clearArtwork(audioFilePathList = []):
  """Clear images added to the given MP3 files.

  Arguments:
    audioFilePathList (list(str)): List of paths to the MP3 files
  """
  for audioFilePath in audioFilePathList:
    if not os.path.isfile(audioFilePath):
      logging.error(f'Not a valid MP3 file: {audioFilePath}')
      continue
    os.system(f'eyeD3 --remove-all-images "{audioFilePath}"')
    logging.info(f'Successfully cleared images for {audioFilePath}')

def createThumbnails(artworkFilePathList, thumbnailsFolder):
  """Create 300x300px thumbnail equivalents.

  Notes:
    The same proportion will be kept.
    The maximum size of either dimension will be 300px.

  Arguments:
    artworkFilePathList (list(str)): File paths of valid artwork files
    thumbnailsFolder (str): Path to the thumbnails folder, guaranteed

  Returns:
    list(str): File names of valid thumbnail files
  """
  thumbnailsFileList = []
  for artworkFilePath in artworkFilePathList:
    _, fileName = os.path.split(artworkFilePath)
    thumbnailFilePath = os.path.join(thumbnailsFolder, fileName)
    os.system(f'convert -resize 300x300 "{artworkFilePath}" "{thumbnailFilePath}"')

    if not os.path.isfile(thumbnailFilePath):
      logging.error(f'Thumbnail not created at {thumbnailFilePath}')
      continue

    logging.info(f'Thumbnail was created for {fileName}')
    thumbnailsFileList.append(thumbnailFilePath)
  return thumbnailsFileList

def addArtwork(musicFilePathList, thumbnailFilePathList):
  """Add thumbnails to all music files.

  Arguments:
    musicFilePathList (list(str)): File paths to valid music files
    thumbnailFilePathList (list(str)): File paths to valid thumbnail files

  Notes:
    `musicFilePathList` should match `thumbnailFilePathList` excluding file extension differences
  """
  pairedFilePathList = zip(musicFilePathList, thumbnailFilePathList)
  for mp3FilePath, pngFilePath in pairedFilePathList:
    os.system(f'eyeD3 --add-image "{pngFilePath}:FRONT_COVER" "{mp3FilePath}"')
    logging.info('Thumbnail added to {mp3File}')

if __name__ == "__main__":
  logging.getLogger().setLevel(logging.INFO)

  thisScriptFolderName = os.path.dirname(os.path.abspath(__file__))

  artworkFolder = os.path.join(thisScriptFolderName, 'Artwork')
  musicFolder = os.path.join(thisScriptFolderName, 'Music')
  thumbnailsFolder = os.path.join(thisScriptFolderName, 'Thumbnails')

  validateFolderStructure(artworkFolder, musicFolder, thumbnailsFolder)

  # Do everything
  if len(sys.argv) == 1:
    artworkFilePathList, musicFilePathList = getOriginalPairedFilePaths(artworkFolder, musicFolder)
    thumbnailFilePathList = createThumbnails(artworkFilePathList, thumbnailsFolder)
    addArtwork(musicFilePathList, thumbnailFilePathList)
  
  # Perform a particular action. Argument(s) must be wrapped in quotes.
  # Argument(s) must give the path to the file
  elif len(sys.argv) > 2:
    mode = sys.argv[1]
    
    # Expecting Music file path arguments
    if mode == 'clear':
      clearArtwork(sys.argv[2:])
    
    # Expecting Music file path arguments
    elif mode == 'add':
      musicFilePathList = validateFilePaths(sys.argv[2:], '.mp3')
      artworkFilePathList = convertEquivalents(musicFilePathList, '.png', artworkFolder)
      thumbnailFilePathList = createThumbnails(artworkFilePathList, thumbnailsFolder)
      addArtwork(musicFilePathList, thumbnailFilePathList)
    
    # Expecting Artwork file path arguments
    elif mode == 'create':
      artworkFilePathList = validateFilePaths(sys.argv[2:], '.png')
      createThumbnails(artworkFilePathList, thumbnailsFolder)
    
    else:
      logging.fatal(f'Unknown mode: {mode}')

  else:
    logging.fatal('Counting the script as an argument... '
      'Need exactly 1 argument or more than 2 arguments')

