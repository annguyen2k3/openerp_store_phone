# -*- coding: utf-8 -*- #su dung bo ma Unicode
from openerp.osv import fields,osv

class invoice_line (osv.osv):
    _name='store_phone.invoice.line'

    _columns = {
        'invoice_id': fields.many2one('store_phone.invoice', 'Hóa đơn', required=True, ondelete='cascade'),
        'product_id': fields.many2one('store_phone.product', 'Sản phẩm', required=True),
        'quantity': fields.integer('Số lượng', required=True),
        'price': fields.float('Giá bán', required=True),
        'amount': fields.function(
            lambda self, cr, uid, ids, field_name, arg, context=None: {
                rec.id: (rec.quantity or 0) * (rec.price or 0) for rec in self.browse(cr, uid, ids, context=context)
            },
            type='float',
            string='Thành tiền',
            store=False
        ),
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

    def _check_stock(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            if record.product_id and record.quantity > (record.product_id.stock or 0):
                # Raise warning with dynamic stock left
                raise osv.except_osv(
                    'Hàng trong kho không đủ',
                    'Còn lại: %d sản phẩm' % (record.product_id.stock or 0)
                )
        return True

    _constraints = [
        (_check_quantity, 'Số lượng phải lớn hơn 0!', ['quantity']),
        (_check_price, 'Giá bán không hợp lệ!', ['price']),
        (_check_stock, 'Hàng trong kho không đủ!', ['quantity']),
    ]

    def create(self, cr, uid, vals, context=None):
        res = super(invoice_line, self).create(cr, uid, vals, context=context)
        product_obj = self.pool.get('store_phone.product')
        product_id = vals.get('product_id')
        quantity = vals.get('quantity', 0)
        if product_id and quantity:
            product = product_obj.browse(cr, uid, product_id, context=context)
            new_stock = (product.stock or 0) - quantity
            product_obj.write(cr, uid, [product_id], {'stock': new_stock}, context=context)
        return res
    
invoice_line()
