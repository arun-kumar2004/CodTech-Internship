const Order = require('../models/Order');

exports.createOrder = async (req, res) => {
  try {
    const { userId, productId, quantity } = req.body;
    const order = await Order.create({ UserId: userId, ProductId: productId, quantity });
    res.json(order);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

exports.getOrders = async (req, res) => {
  const orders = await Order.findAll();
  res.json(orders);
};
