#!/usr/bin/env python3
"""
Debug script to verify financial calculations
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Shipment, ExpenseGeneral, FinancialTransaction, GlobalSettings

def debug_calculations():
    with app.app_context():
        print("=== تشخيص الحسابات المالية ===")
        
        # Get the single shipment
        shipment = Shipment.query.first()
        if not shipment:
            print("لا توجد شحنات")
            return
            
        print(f"الشحنة: {shipment.tracking_number}")
        print(f"النوع: {shipment.package_type}")
        print(f"المبلغ المدفوع: {shipment.paid_amount} د.ك")
        print(f"الوزن: {shipment.weight} كيلو")
        print()
        
        # Calculate category expenses
        category_expenses = shipment.calculate_category_expenses_for_report()
        print(f"مصروفات الفئة (المحسوبة): {category_expenses} د.ك")
        
        # Break down the calculation for general shipments
        if shipment.package_type != 'document':
            print("\n--- تفصيل حساب المصروفات للشحنة العامة ---")
            
            # Total general expenses
            total_general = shipment.get_total_general_category_expenses()
            print(f"إجمالي المصروفات العامة: {total_general} د.ك")
            
            # Cost per kg
            cost_per_kg = float(GlobalSettings.get_setting('cost_per_kg', 0.0))
            print(f"تكلفة الكيلو: {cost_per_kg} د.ك")
            
            # Weight cost
            weight_cost = cost_per_kg * float(shipment.weight) if shipment.weight else 0.0
            print(f"تكلفة الوزن: {cost_per_kg} × {shipment.weight} = {weight_cost} د.ك")
            
            # Total expenses
            total_expenses = total_general + weight_cost
            print(f"إجمالي المصروفات: {total_general} + {weight_cost} = {total_expenses} د.ك")
            
            # Net profit
            net_profit = float(shipment.paid_amount) - total_expenses
            print(f"صافي الربح: {shipment.paid_amount} - {total_expenses} = {net_profit} د.ك")
            
        print("\n--- حساب الربح باستخدام الدالة ---")
        calculated_profit = shipment.calculate_net_profit_for_report()
        print(f"صافي الربح (محسوب): {calculated_profit} د.ك")
        
        print("\n--- التحقق من بيانات المصروفات ---")
        # Check expenses
        general_expenses = ExpenseGeneral.query.all()
        print(f"عدد المصروفات العامة: {len(general_expenses)}")
        for exp in general_expenses:
            print(f"  - {exp.name}: {exp.amount} د.ك")
            
        financial_expenses = FinancialTransaction.query.filter_by(
            transaction_type='expense',
            shipping_type='شحنات عامة'
        ).all()
        print(f"عدد المصروفات المالية: {len(financial_expenses)}")
        for exp in financial_expenses:
            print(f"  - {exp.name}: {exp.amount} د.ك")
        
        print("\n--- النتيجة المتوقعة ---")
        print(f"الإيرادات: {shipment.paid_amount} د.ك")
        print(f"المصروفات: {category_expenses} د.ك")
        print(f"صافي الربح: {calculated_profit} د.ك")
        
        print("\n--- التصحيحات المطلوبة ---")
        print("قبل التصحيح (الأرقام الخاطئة في الصورة):")
        print("- صافي الإيرادات: 12.5 د.ك ❌")
        print("- إجمالي المصروفات: 2.5 د.ك ❌")
        print("- إجمالي الأرباح: 15.0 د.ك ❌")
        
        print("\nبعد التصحيح (الأرقام الصحيحة):")
        print(f"- صافي الإيرادات: {shipment.paid_amount} د.ك ✅")
        print(f"- إجمالي المصروفات: {category_expenses} د.ك ✅")
        print(f"- إجمالي الأرباح: {calculated_profit} د.ك ✅")

if __name__ == "__main__":
    debug_calculations()