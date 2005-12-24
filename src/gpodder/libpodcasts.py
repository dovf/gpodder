
#
# gPodder
# Copyright (c) 2005 Thomas Perl <thp@perli.net>
# Released under the GNU General Public License (GPL)
#

#
#  libpodcasts.py -- data classes for gpodder
#  thomas perl <thp@perli.net>   20051029
#
#

import gtk
import gobject


# podcastChannel: holds data for a complete channel
class podcastChannel(object):
    url = ""
    title = ""
    link = ""
    description = ""
    items = []
    image = None
    shortname = None

    def __init__( self, url = "", title = "", link = "", description = ""):
        self.url = url
        self.title = title
        self.link = link
        self.description = description
        self.items = []
    
    def addItem( self, item):
        self.items.append( item)
    
    def printChannel( self):
        print "- Channel: \"" + self.title + "\""
        for item in self.items:
            print "-- Item: \"" + item.title + "\""

    def isDownloaded( self, item):
        from libgpodder import gPodderLib
        return gPodderLib().podcastFilenameExists( self, item.url)

    def getItemsModel( self):
        new_model = gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)

        for item in self.items:
            # Skip items with no download url
            if item.url != "":
                if self.isDownloaded(item):
                    background_color = "#eeeeee"
                else:
                    background_color = "white"
                new_iter = new_model.append()
                new_model.set( new_iter, 0, item.url)
                new_model.set( new_iter, 1, item.title)
                new_model.set( new_iter, 2, item.getSize())
                new_model.set( new_iter, 3, True)
                new_model.set( new_iter, 4, background_color)
        
        return new_model
    
    def getActiveByUrl( self, url):
        i = 0
        
        for item in self.items:
            if item.url == url:
                return i
            i = i + 1

        return -1


# podcastItem: holds data for one object in a channel
class podcastItem(object):
    url = ""
    title = ""
    length = ""
    mimetype = ""
    guid = ""
    description = ""
    link = ""
    
    def __init__( self, url = "", title = "", length = "0", mimetype = "", guid = "", description = "", link = ""):
        self.url = url
        self.title = title
        self.length = length
        self.mimetype = mimetype
        self.guid = guid
        self.description = description
        self.link = ""
    
    def getSize( self):
        kilobyte = 1024
        megabyte = kilobyte * 1024
        gigabyte = megabyte * 1024

        size = int( self.length)
        if size > gigabyte:
            return str( size / gigabyte) + " GB"
        if size > megabyte:
            return str( size / megabyte) + " MB"
        if size > kilobyte:
            return str( size / kilobyte) + " KB"

        return str( size) + " Bytes"


class configChannel( object):
    title =""
    url =""
    filename = None

    def __init__( self, title = "", url = "", filename = None):
        self.title = title
        self.url = url
        
        if filename == None:
            self.filename = self.createFilename()
        else:
            self.filename = filename
    
    def createFilename( self):
        result = ""

        for char in self.title.lower():
            if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z') or (char >= '1' and char <= '9'):
                result = result + char

        return result


def channelsToModel( channels):
    new_model = gtk.ListStore( gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_OBJECT)
    
    for channel in channels:
        new_iter = new_model.append()
        new_model.set( new_iter, 0, channel.url)
        new_model.set( new_iter, 1, channel.title + " ("+channel.url+")")
        #if channel.image != None:
        #    new_model.set( new_iter, 2, gtk.gdk.pixbuf_new_from_file_at_size( channel.image, 60, 60))
        #else:
        #    new_model.set( new_iter, 2, None)
    
    return new_model


