#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

##############################################################################
# customize directories to automatically find and register software

def dirs(i):
    import os

    dr=i.get('dirs',[])

    ck_os_name=i.get('host_os_dict',{}).get('ck_name','')
    if ck_os_name=='win':
       local_app_data = os.getenv('LOCALAPPDATA')
       if local_app_data is not None:
          dr.append(local_app_data)

       roaming_app_data = os.getenv('APPDATA')
       if roaming_app_data is not None:
          dr.append(roaming_app_data)

       for px in ['C:\\', 'D:\\']:
           x=[]
           try:
              x=os.listdir(px)
           except:
              pass

           for q in x:
               qq=os.path.join(px,q)
               if os.path.isdir(qq) and q.lower().startswith('python'):
                  dr.append(qq)

    return {'return':0}

##############################################################################
# limit directories 

def limit(i):

    import os

    dr=i.get('list',[])
    drx=[]

    for q in dr:
        q1=os.path.basename(q)
        if q.endswith('.exe'):
           q1=q1[:-4]
        if q.find('X11')<0:
           if q1=='python' or q1=='python2' or q1=='python3':
              drx.append(q)

    return {'return':0, 'list':drx}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip()
        if q!='' and q.startswith('Python ') and len(q)>6:
           ver=q[7:]

           j=ver.find(' ::')
           if j>0:
              ver=ver[:j]   
           break

    return {'return':0, 'version':ver}

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    import os

    # Get variables
    ck=i['ck_kernel']
    s=''

    cus=i['customize']
    env=i['env']

    host_d=i.get('host_os_dict',{})
    winh=host_d.get('windows_base','')

    ver=i.get('version','')
    sver=i.get('version_split',[])

    fp=cus.get('full_path','')

    ep=cus['env_prefix']

    p1=os.path.dirname(fp)
    p2=os.path.dirname(p1)

    env[ep]=p2
    env[ep+'_FILE']=fp
    env[ep+'_BIN']=p1

    # Check version
    mf=os.path.basename(fp)
    env['CK_PYTHON_BIN']=mf

    if mf.endswith('.exe'): mf=mf[:-4]

    pver=''
    if len(sver)>0:
       if sver[0]==2:
          pver='2'
       elif sver[0]==3:
          pver='3'
    elif mf.endswith('2'):
       pver='2'
    elif mf.endswith('3'):
       pver='3'

    if pver=='2':
       env['CK_PYTHON_VER2']='YES'
    elif pver=='3':
       env['CK_PYTHON_VER3']='YES'

    # Checking pip
    lpip=[]

    lpip.append(('pip'+pver,p1))
    lpip.append(('pip'+pver,os.path.join(p2,'local','bin')))
    lpip.append(('pip'+pver,os.path.join(p1,'Scripts')))

    lpip.append(('pip',p1))
    lpip.append(('pip',os.path.join(p2,'local','bin')))
    lpip.append(('pip',os.path.join(p1,'Scripts')))

    found=False
    for x in lpip:
        pip=x[0]
        if winh=='yes': pip+='.exe'
        ppip=os.path.join(x[1],pip)
        if os.path.isfile(ppip): 
           found=True
           break

    if found:
       env['CK_PYTHON_PIP_BIN']=pip
       env['CK_PYTHON_PIP_BIN_FULL']=ppip

    ############################################################
    if winh=='yes':
       s+='\nset PATH='+p1+';'+p1+'\\Scripts;%PATH%\n\n'
    else:
       s+='\nexport PATH='+p1+':'+p1+'/Scripts:$PATH\n\n'

    return {'return':0, 'bat':s}
