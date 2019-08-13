#ifndef RUNMODEL_H
#define RUNMODEL_H

#include <QObject>

using namespace std;

class RunModel : public QObject
{
  Q_OBJECT
  Q_PROPERTY(QString script READ script NOTIFY scriptChanged)
  Q_PROPERTY(double frameHeight READ frameHeight WRITE setFrameHeight NOTIFY frameChanged)
  Q_PROPERTY(double frameWidth READ frameWidth WRITE setFrameWidth NOTIFY frameChanged)
  Q_PROPERTY(QString horizontalCommand READ horizontalCommand WRITE setHorizontalCommand NOTIFY scriptChanged)
  Q_PROPERTY(QString verticalCommand READ verticalCommand WRITE setVerticalCommand NOTIFY scriptChanged)

 public:
  explicit RunModel(QObject *parent = nullptr);

  QString script();
  double frameHeight();
  void setFrameHeight(double w);
  double frameWidth();
  void setFrameWidth(double w);
  QString verticalCommand();
  void setVerticalCommand(QString w);
  QString horizontalCommand();
  void setHorizontalCommand(QString w);

 signals:
  void scriptChanged();
  void frameChanged();
 private:
  double m_frameHeight;
  double m_frameWidth;
  QString m_horizontalCommand;
  QString m_verticalCommand;
};

#endif
