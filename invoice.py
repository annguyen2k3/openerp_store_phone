# -*- coding: utf-8 -*- #su dung bo ma Unicode
from openerp.osv import fields,osv

class invoice (osv.osv):
    _name='store_phone.invoice'

    _columns = {
        'customer_name' : fields.char('Tên khách hàng', size=250, required=True, translate=True),
        'customer_address' : fields.char('Địa chỉ khách hàng', size=250, translate=True),
        'customer_phone' : fields.char('Điện thoại khách hàng', size=25, translate=True),
        'line_ids' : fields.one2many('store_phone.invoice.line', 'invoice_id', 'Chi tiết hóa đơn'),
        'payment_method' : fields.selection([
            ('cash', 'Tiền mặt'),
            ('bank', 'Chuyển khoản')
        ], 'Phương thức thanh toán', required=True),
        'date' : fields.date('Ngày lập hóa đơn', required=True),
        'total_amount': fields.function(
            lambda self, cr, uid, ids, field_name, arg, context=None: {
                rec.id: sum(line.amount for line in rec.line_ids) for rec in self.browse(cr, uid, ids, context=context)
            },
            type='float',
            string='Tổng tiền',
            store=False
        ),
    }

    _defaults = {
        'date': fields.date.context_today,
    }
    
invoice()
