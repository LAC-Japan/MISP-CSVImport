# MISP CSVImport

MISP project: <http://www.misp-project.org/>

## Overview

Register MISP events based on information described in files such as CSV and TSV.  

## license

This software is released under the BSD License, see LICENSE.txt.

## Environment

* Python 3.5.2 and above  
* Pymisp 2.4.85 or higher  

## usage

#### 1 Creating a file for import

##### 1-1 File Format

In the target file, please describe the items in the following order with an arbitrary delimiter. A header line is not required.  
(TSV recommended)  

* Date  
* Organization  
* User  
* Title  
* Tag1  
* Tag2  
* Tag3  
* Tag4  
* Value  
* Category  
* Type  
* Attribute_tags  
* Comment  

##### Example

sample.tsv

##### 1-2 Mapping of file items and MISP events

Each item is mapped to the MISP event with the following contents.  

* Date: date of the event  
* Organization: registered user's organization. It is not taken into account in the script. Please correctly register when creating the corresponding user.  
* User: User mail address used for registration. It is necessary to link with this mail address when defining authkey with const.  
* Title: event info. For lines with the same value, they are handled as one event, and all tagged information and attribute information is added to the same event.  
* Tag1: Tag of the event. Multiple tags can be specified by separating them with ",".  
* Tag 2: tag of the event. Multiple tags can be specified by separating them with ",".  
* Tag 3: tag of the event. Multiple tags can be specified by separating them with ",".  
* Tag 4: tag of the event. Multiple tags can be specified by separating them with ",".  
* Value: Value of the attribute  
* Category: attribute Category  
* type-Type of the attribute  
* attribute_tags: The tag of the attribute. Multiple tags can be specified by separating them with ",".  
* Comment: An attribute comment.  

#### 2 Setting const.py

Open const.py and make the following settings.  

##### 2-1 MISP connection

* MISP_URL: URL of server running MISP  

##### 2-2 Import configuration

In the following variables, set the user's mail address as the key and the import setting for the user as the value in the following format.
The user mail address defined here is associated with the value in the user column of the import control file, and the import setting of that user is used when importing the corresponding event.
target: IMPORT_CONFIG

##### example

    IMPORT_CONFIG = {
    	'sample@misp.user': {
    		'authkey': 'valid authkey'
    		,'distribution': 'distribution config constants'
    		,'threat_level': 'threat level config constants'
    		,'analysis_level': 'analysis level config constants'
    	}
    }

#### 3 Running the script

` python3 ./MISP-CSVImport.py - i [import file path] [option] `

##### Option

* -i: Import file path. Required.  
* --cs: Column delimiter. Default "\ t"  
* --ls: New line character. Default "\n"  
* --skip-header: skip header row.default False  
* --target-row: Start line to be imported. Line breaks that exist in the value enclosed by" "are not included in the line number, so please specify it in units of the number of lines to be imported. When omitted, all data is targeted from the first line.  

##### example

Import sample.tsv
` python3 ./MISP-CSVImport.py -i ./sample.tsv --skip-header --ls "\r\n" --cs "	" `

## Precautions

* If an event with the same title as the event title you are trying to import exists on MISP, the existing event is deleted and new contents are registered  
* For tags described as tags of events or attributes, add them as tags if they are not registered in MISP, then set them as tags of the corresponding event or attribute. Therefore, the user who performs the import needs "add tag" authority.  
* If there is a line whose attribute / category / type / value all match in the same event title in the data to be imported, a warning is displayed and the corresponding line is ignored  
* Registration errors due to input data such as inconsistency of attribute category / type may be output, so please check all the output results of the script  
* When multibyte characters are included in the import file, please make the character code with UTF-8(no BOM)  
* If you want to include line breaks in each field of the file, enclose the corresponding field with ""  
