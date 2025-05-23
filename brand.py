# -*- coding: utf-8 -*- #su dung bo ma Unicode
from openerp.osv import fields,osv

class brand (osv.osv):
    _name='store_phone.brand'

    _rec_name = 'name'

    _columns = {
        'code': fields.char('Mã thương hiệu', size=25, required=True, translate=True),
        'name': fields.char('Tên thương hiệu', size=100, required=True, translate=True),
        'description': fields.text('Mô tả', translate=True),
        'product_ids': fields.one2many('store_phone.product', 'brand_id', 'Danh sách sản phẩm'),
    }

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Mã thương hiệu đã tồn tại!'),
    ]
    
brand()
