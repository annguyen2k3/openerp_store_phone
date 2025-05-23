# -*- coding: utf-8 -*- #su dung bo ma Unicode
from openerp.osv import fields,osv

class purchase (osv.osv):
    _name='store_phone.purchase'

    _columns = {
        'product_id' : fields.many2one('store_phone.product', 'Sản phẩm', required=True),
        'quantity' : fields.integer('Số lượng', required=True),
        'price' : fields.float('Giá nhập', required=True),
        'supplier' : fields.char('Nhà cung cấp', size=250, required=True, translate=True),
        'date' : fields.date('Ngày nhập', required=True),
        'note' : fields.text('Ghi chú', translate=True),
        'total_amount': fields.function(
            lambda self, cr, uid, ids, field_name, arg, context=None: {
                rec.id: rec.quantity * rec.price for rec in self.browse(cr, uid, ids, context=context)
            },
            type='float',
            string='Tổng tiền',
            store=False
        ),
    }

    _defaults = {
        'date': fields.date.context_today,
    }

    def _check_quantity(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            if record.quantity <= 0:
                return False
        return True

    def _check_price(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            if record.price < 0:
                return False
        return True

    _constraints = [
        (_check_quantity, 'Số lượng phải lớn hơn 0!', ['quantity']),
        (_check_price, 'Giá nhập không hợp lệ!', ['price']),
    ]
    
    def create(self, cr, uid, vals, context=None):
        purchase_id = super(purchase, self).create(cr, uid, vals, context=context)
        product_obj = self.pool.get('store_phone.product')
        product_id = vals.get('product_id')
        quantity = vals.get('quantity', 0)
        if product_id and quantity:
            product = product_obj.browse(cr, uid, product_id, context=context)
            new_stock = (product.stock or 0) + quantity
            product_obj.write(cr, uid, [product_id], {'stock': new_stock}, context=context)
        return purchase_id

purchase()
