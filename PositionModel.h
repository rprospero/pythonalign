#ifndef POSITIONMODEL_H
#define POSITIONMODEL_H

#include <QObject>

class PositionModel : public QObject
{
  Q_OBJECT
  Q_PROPERTY(qreal width READ width WRITE setWidth NOTIFY realigned)

 public:
  explicit PositionModel(QObject *parent = nullptr);

  qreal width();
  void setWidth(qreal w);

 signals:
  void realigned();
 private:
  qreal m_width;
};

#endif
