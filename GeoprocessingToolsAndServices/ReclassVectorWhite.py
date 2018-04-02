# Python script: ReclassVectorWhite.py

# This script outputs/returns a Feature Class with data from 'orig_shapefile' and adds an attribute called 'outfield'
#  whose values are reclassified values from 'infield', based on ranges in a database table file (.dbf) called 'reclasstable'.
#  (if the value is not found based on ranges in 'reclasstable', it is reclassified as 'notfoundvalue')

# import the ArcPy package
import arcpy

# define path for 'orig_shapefile'
orig_shapefile = arcpy.GetParameterAsText(0)

# define path to 'new_shapefile'
new_shapefile = arcpy.GetParameterAsText(1)

# make a copy of 'orig_shapefile'
arcpy.CopyFeatures_management(orig_shapefile, new_shapefile)

# define 'infield' that's in orig_shapefile, this will be used for reclassification
infield = arcpy.GetParameterAsText(2)

arcpy.AddMessage("Field to be reclassified: "+infield)

# create field 'outfield' and add it to a 'new_shapefile'
outfield = arcpy.GetParameterAsText(3)
arcpy.AddField_management(new_shapefile, outfield, 'DOUBLE')

arcpy.AddMessage("Reclassified field: "+outfield)

# define path to 'reclasstable' (a .dbf file (table)), this will be used for reclassification
reclasstable = arcpy.GetParameterAsText(4)

# define 'notfoundvalue', to be used if value of 'infield' is not found in 'reclasstable' (default is 9999)
notfoundvalue = arcpy.GetParameterAsText(5)

# add 'outfield' to 'new_shapefile'
arcpy.AddField_management(new_shapefile, outfield, 'DOUBLE')

# prints out fields in the shapefile
# print "Fields in the file: " + new_shapefile
# fields = arcpy.ListFields(new_shapefile)
# for field in fields:
#	print field.name
# print ''

# create search cursor to read through 'reclasstable'
tblcursor = arcpy.da.SearchCursor(reclasstable, ['lowerbound', 'upperbound', 'value'])

# create update cursor to update 'outfield' with new classification based on 'infield'
update_cursor = arcpy.da.UpdateCursor(new_shapefile, [infield, outfield])

# print 'BEFORE reclassification: '
# i = 1
# for row in update_cursor:
#	print 'Row ' + str(i) + ' :: AREA: ' + str(row[0]) + ', RECLASS: ' + str(row[1])
#	i += 1
# print ''

# reset 'update_cursor' back to the first row
# update_cursor.reset()

# loops through each row in 'new_shapefile' ... looks at the value of 'infield' and decides what to write in the 'outfield', using the data from 'reclasstable':
for shprow in update_cursor:
	checkvalue = shprow[0]
	
	# reset 'tblcursor' back to the first row
	tblcursor.reset()
	
	# loops through each row in 'reclasstable' and finds the first row where the value of 'infield' is >= 'lowerbound' and <= 'upperbound':
	#  if this row exists: 'outfield' = value,  
	#  and if no row exists: 'outfield' = 'notfoundvalue'
	for tblrow in tblcursor:
		lowerbound = tblrow[0]
		upperbound = tblrow[1]
		value = tblrow[2]
		if checkvalue >= lowerbound and checkvalue <= upperbound:
			shprow[1] = value
			update_cursor.updateRow(shprow)
			
			# exit loop if 'infield' is found within ranges in 'reclasstable'
			break

		else:
			shprow[1] = notfoundvalue
			update_cursor.updateRow(shprow)

# reset 'update_cursor' back to the first row
# update_cursor.reset()

# print 'AFTER reclassification: '
# i = 1
# for row in update_cursor:
#     print 'Row ' + str(i) + ' :: AREA: ' + str(row[0]) + ', RECLASS: ' + str(row[1])
#     i += 1

# delete cursors to avoid errors
del tblcursor

del update_cursor
