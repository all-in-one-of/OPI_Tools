import os
import sys
import maya
import maya.cmds as cmds
import maya.OpenMaya
import maya.OpenMayaMPx

import pymel
import pymel.core

def onSceneDefaults(userdata):

  # set units
  maya.cmds.currentUnit(linear='cm', angle='deg', time='pal')
  print '\n---------------------------------\nTom Sporer defaults set\n---------------------------------'

def setProjectPath():
  # set the project path
  filePath = maya.cmds.file(q=True, sn=True)
  folder = os.path.split(filePath)[0]
  while folder:
    workspace = os.path.join(folder, 'workspace.mel')
    if os.path.exists(workspace):
      pymel.core.mel.eval('setProject "%s"' % folder.replace("\\", '/'))
      break
    if folder == os.path.split(folder)[0]:
      break
    folder = os.path.split(folder)[0]

def checkForRenderSetupMismatch():
  # Check Preferred Render Setup System in Maya Preferences
  prefRenderSetup = cmds.optionVar(q="renderSetupEnable")
  # 1 = New Render Setup
  # 0 = Legacy Render Layers

  # Check Render Setup System in current Scene
  renderLayers = cmds.ls( type="renderLayer" )
  renderLayers.remove("defaultRenderLayer")
  try:
    renderSetupLayers = cmds.ls( type="renderSetupLayer" )
  except:
    renderSetupLayers = []

  if prefRenderSetup == 1:
    if len(renderLayers) > len(renderSetupLayers):
      renderSetupWarning(1)
  else:
    if len(renderSetupLayers) > 0:
      renderSetupWarning(0)

def renderSetupWarning(prefRenderSetup):
  if prefRenderSetup == 1:
    dialogMsg = "Warning: This file contains legacy render layers and Maya is currently in Render Setup mode."
  else:
    dialogMsg = "Warning: This file contains render setup nodes and Maya is currently in Legacy Render Layers mode."
  dialog = cmds.confirmDialog(title="Render Setup Mismatch", message=dialogMsg, button="That's too bad", cancelButton="That's too bad", dismissString="That's too bad", icon="warning")

def onSceneLoad(userdata):
  onSceneDefaults(userdata)
  setProjectPath()
  checkForRenderSetupMismatch()

def onSceneSave(userdata):
  setProjectPath()

def initializePlugin(mobject):
  mplugin = maya.OpenMayaMPx.MFnPlugin(mobject)

  try:
    globals()['ts_gOnSceneNewCallbackId'] = maya.OpenMaya.MSceneMessage.addCallback(maya.OpenMaya.MSceneMessage.kAfterNew, onSceneDefaults);
  except Exception as e:
    sys.stderr.write('Failed to register kAfterNew callback.')
    raise

  try:
    globals()['ts_gOnSceneLoadCallbackId'] = maya.OpenMaya.MSceneMessage.addCallback(maya.OpenMaya.MSceneMessage.kAfterOpen, onSceneLoad);
  except Exception as e:
    sys.stderr.write('Failed to register kAfterOpen callback.')
    raise

  try:
    globals()['ts_gOnSceneSaveCallbackId'] = maya.OpenMaya.MSceneMessage.addCallback(maya.OpenMaya.MSceneMessage.kAfterSave, onSceneSave);
  except Exception as e:
    sys.stderr.write('Failed to register kAfterSave callback.')
    raise

def uninitializePlugin(mobject):
  mplugin = maya.OpenMayaMPx.MFnPlugin(mobject)

  try:
    maya.OpenMaya.MSceneMessage.removeCallback(globals()['ts_gOnSceneNewCallbackId'])
  except:
    sys.stderr.write('Failed to remove kAfterNew callback.')
    raise

  try:
    maya.OpenMaya.MSceneMessage.removeCallback(globals()['ts_gOnSceneLoadCallbackId'])
  except:
    sys.stderr.write('Failed to remove kAfterOpen callback.')
    raise

  try:
    maya.OpenMaya.MSceneMessage.removeCallback(globals()['ts_gOnSceneSaveCallbackId'])
  except:
    sys.stderr.write('Failed to remove kAfterSave callback.')
    raise
