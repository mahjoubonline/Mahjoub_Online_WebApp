@staticmethod
    def fetch_and_sync_order():
        logger.info("🔄 بدء المزامنة المصححة مع قمرة...")
        
        # استعلام مصحح بناءً على متطلبات GraphQL الصارمة
        query = """
        query {
            findAllOrders(input: {}) {
                data {
                    _id
                    totalPrice
                    status {
                        code
                    }
                    financialStatus
                    fulfillmentStatus
                    createdAt
                    customer {
                        name
                        shippingAddress
                    }
                    items {
                        _id
                        quantity
                    }
                }
            }
        }
        """
        
        try:
            response = requests.post(SyncEngine.API_URL, json={'query': query}, headers=SyncEngine._get_headers(), timeout=120)
            result = response.json()
            
            if 'errors' in result:
                logger.error(f"❌ خطأ GraphQL تفصيلي: {result['errors']}")
                return False
            
            orders_data = result.get('data', {}).get('findAllOrders', {}).get('data', [])
            
            for item in orders_data:
                id_api = str(item.get('_id'))
                if not id_api: continue
                    
                order = ProcessedOrder.query.filter_by(id=id_api).first() or ProcessedOrder(id=id_api)
                
                order.order_id = id_api[:8]
                order.total_price = float(item.get('totalPrice') or 0.0)
                
                # تصحيح الوصول للحالة: الـ API يطلب حقول فرعية لـ status
                status_obj = item.get('status') or {}
                order.order_status = status_obj.get('code', 'pending')
                
                customer = item.get('customer') or {}
                order.customer_name = customer.get('name', 'عميل غير معروف')
                order.shipping_city = customer.get('shippingAddress', '---')
                
                order.items_count = len(item.get('items') or [])
                order.financial_status = item.get('financialStatus') or 'unpaid'
                order.fulfillment_status = item.get('fulfillmentStatus') or 'unfulfilled'
                
                db.session.add(order)
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ فشل المزامنة: {e}")
            return False
