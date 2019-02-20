#-------------------------------------------------
#
# Project created by QtCreator 2016-06-07T18:10:12
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = qt-test
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    camviewer.cpp

HEADERS  += mainwindow.h \
    camviewer.h

FORMS    += mainwindow.ui

INCLUDEPATH += /usr/local/include
LIBS += -L/usr/local/lib \
     -lopencv_core \
     -lopencv_imgproc \
     -lopencv_videoio \
     -lopencv_highgui \
     -lopencv_objdetect

#QT_CONFIG -= no-pkg-config
#CONFIG  += link_pkgconfig
#PKGCONFIG += opencv
