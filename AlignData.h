#ifndef ALIGNDATA_H
#define ALIGNDATA_H

#include <QObject>
#include <QPointF>

class AlignData : public QObject
{
  Q_OBJECT
  Q_PROPERTY(qreal width READ width WRITE setWidth NOTIFY realigned)
  Q_PROPERTY(qreal height READ height WRITE setHeight NOTIFY realigned)
  Q_PROPERTY(qreal newsize READ newsize WRITE setNewsize NOTIFY realigned)
  Q_PROPERTY(QPointF p1 READ p1 WRITE setP1 NOTIFY realigned)
  Q_PROPERTY(QPointF p2 READ p2 WRITE setP2 NOTIFY realigned)
  Q_PROPERTY(QPointF p3 READ p3 WRITE setP3 NOTIFY realigned)
  Q_PROPERTY(QPointF p4 READ p4 WRITE setP4 NOTIFY realigned)

 public:
  explicit AlignData(QObject *parent = nullptr);

  qreal width();
  void setWidth(qreal w);
  qreal height();
  void setHeight(qreal w);
  qreal newsize();
  void setNewsize(qreal w);
  QPointF p1();
  void setP1(QPointF w);
  QPointF p2();
  void setP2(QPointF w);
  QPointF p3();
  void setP3(QPointF w);
  QPointF p4();
  void setP4(QPointF w);

 signals:
  void realigned();
 private:
  qreal m_width;
  qreal m_height;
  qreal m_newsize;
  QPointF m_p1;
  QPointF m_p2;
  QPointF m_p3;
  QPointF m_p4;
};

#endif
