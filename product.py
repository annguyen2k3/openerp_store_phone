# -*- coding: utf-8 -*- #su dung bo ma Unicode
from openerp.osv import fields,osv

class product (osv.osv):
    _name='store_phone.product'

    _rec_name = 'name'

    _columns = {
        'name' : fields.char('Tên sản phẩm', size=250, required=True, translate=True),
        'code' : fields.char('Mã sản phẩm', size=25, required=True, translate=True),
        'brand_id' : fields.many2one('store_phone.brand', 'Thương hiệu'),
        'price' : fields.float('Giá sản phẩm', required=True),
        'description' : fields.text('Mô tả', translate=True),
        'actived' : fields.boolean('Trạng thái'),
        'stock' : fields.integer('Số lượng tồn kho', readonly=True),
    }

    _defaults={
        'actived': True,
        'stock': 0,
    }
    
    def _check_price(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            if record.price < 0:
                return False
        return True

    _constraints = [
        (_check_price, 'Giá sản phẩm không hợp lệ!', ['price']),
    ]

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Mã sản phẩm đã tồn tại!'),
    ]

product() 
