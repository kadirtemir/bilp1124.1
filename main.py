import customtkinter, psycopg2, os, re
from CTkMenuBar import *
from PIL import Image, ImageTk
from CTkListbox import *
from datetime import date


class MenuBar:
    def __init__(self, master):

        self.master = master
        self.IconLock = False
        #MENU FRAME'IN OLUSUTURULMASI
        self.master.grid_rowconfigure(0, weight=10)
        self.master.grid_columnconfigure(1, weight=10)
        self.master.mainFrame = customtkinter.CTkFrame(self.master, corner_radius=0, fg_color="#172B4D")
        self.master.mainFrame.grid(row=0, column=0, sticky="nsew")
        self.master.mainFrame.grid_rowconfigure(8, weight=1)
        #Icon İmport
        self.import_icons()

        self.userIconLabel = customtkinter.CTkLabel(master=self.master.mainFrame, image=self.userIcon, text='')
        self.userIconLabel.grid(row=0, column=0, padx=10, pady=(30, 0), columnspan=2)
        navigation_frame_label = customtkinter.CTkLabel(self.master.mainFrame, text="BİLP1124.1 D.B. II", 
                                                        compound="left", font=customtkinter.CTkFont(size=15, weight="bold"), text_color="gray90")
        navigation_frame_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))


        #Butonların Tanımlanması
        home_button = customtkinter.CTkButton(self.master.mainFrame, corner_radius=0, height=40, border_spacing=10, text="Satışlar",
                                            fg_color="transparent", text_color=("gray90", "gray90"),
                                            hover_color=("gray70", "gray30"),
                                            anchor="w", command=self.show_sales_page, image=self.salesIcon)
        home_button.grid(row=2, column=0, sticky="ew")

        create_bid_button = customtkinter.CTkButton(self.master.mainFrame, corner_radius=0, height=40, border_spacing=10,
                                                    text="Ürünler",
                                                    fg_color="transparent", text_color=("gray90", "gray90"),
                                                    hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.show_urunler_sayfa, image=self.productsIcon)
        create_bid_button.grid(row=3, column=0, sticky="ew")


        add_data_button = customtkinter.CTkButton(self.master.mainFrame, corner_radius=0, height=40, border_spacing=10,
                                                    text="Müşteriler",
                                                    fg_color="transparent", text_color=("gray90", "gray90"),
                                                    hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.show_musteriler_sayfa, image=self.customersIcon)
        add_data_button.grid(row=4, column=0, sticky="ew")


        edit_user_button = customtkinter.CTkButton(self.master.mainFrame, corner_radius=0, height=40, border_spacing=10,
                                                    text="Satış Özetleri",
                                                    fg_color="transparent", text_color=("gray90", "gray90"),
                                                    hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.show_total_sayfa, image=self.suppliersIcon)
        edit_user_button.grid(row=5, column=0, sticky="ew")

        appearance_mode_menu = customtkinter.CTkOptionMenu(self.master.mainFrame, values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode_event)
        appearance_mode_menu.grid(row=8, column=0, padx=20, pady=20, sticky="s")

        self.current_page = None

    def import_icons(self):
        if not self.IconLock:
            self.IconLock = True
            self.userIcon = customtkinter.CTkImage(light_image=Image.open(os.path.join("images/icons", "user_icon.png")), size=(100 , 100))
            self.salesIcon = customtkinter.CTkImage(light_image=Image.open(os.path.join("images/icons", "sales.png")), size=(35 , 35))
            self.customersIcon = customtkinter.CTkImage(light_image=Image.open(os.path.join("images/icons", "customers.png")), size=(30 , 30))
            self.suppliersIcon = customtkinter.CTkImage(light_image=Image.open(os.path.join("images/icons", "suppliers.png")), size=(33 , 33))
            self.productsIcon = customtkinter.CTkImage(light_image=Image.open(os.path.join("images/icons", "products.png")), size=(30 , 30))
    

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def show_sales_page(self):
        self.show_page(salesPage, "Ana Sayfa")

    def show_urunler_sayfa(self):
        self.show_page(productsPage, "Ürünler Sayfası")

    def show_musteriler_sayfa(self):
        self.show_page(customersPage, "Müşteriler Sayfası")

    def show_total_sayfa(self):
        self.show_page(totalPage, "Toplam Satışlar Sayfası")

    def show_page(self, page_class, page_name):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = page_class(self.master)




class salesPage(customtkinter.CTkFrame):
    def __init__(self, master):

        self.master = master
        self.master.title("Satışlar Ekranı")
        self.master.geometry("930x600")
 
        MenuBar(self.master)
        
        self.master.sales_frame = customtkinter.CTkFrame(self.master, corner_radius=0, fg_color="transparent")
        self.master.sales_frame.grid_columnconfigure(0, weight=1)
        self.master.sales_frame.grid(row=0, column=1, sticky="nsew")

        sales = selectQuery("SELECT satisid, ad, telefon, urunadi, satistarihi, toplamfiyat  FROM satislar, urunler, musteriler WHERE satislar.urunid = urunler.urunid and satislar.musteriid = musteriler.musteriid;")

        label = customtkinter.CTkLabel(master=self.master.sales_frame, text="Satışlar", font=("Helvetica", 24, "bold"),)
        label.place(x=50, y=60)

        self.addSaleIcon = customtkinter.CTkImage(light_image=Image.open(os.path.join("images/icons", "add.png")), size=(45 , 45))
        self.addSaleIconLabel = customtkinter.CTkLabel(master=self.master.sales_frame, image=self.addSaleIcon, text='')  
        self.addSaleIconLabel.place(x=620, y=58)

        self.salesListbox = CTkListbox(self.master.sales_frame, width=600, height=300, text_color="black")
        self.salesListbox.place(x=50, y=130)

        for sale in sales:
            saleDataForListbox = str(sale[0]) + "-) " + str(sale[1]) + "  " + str(sale[2]) + "  " + str(sale[3]) + "  " + str(sale[4]) + str(sale[5]) + "TL"
            self.salesListbox.insert("END", saleDataForListbox)
        
        customtkinter.CTkButton(master=self.master.sales_frame,
                            width=140,
                            height=45,
                            border_width=0,
                            corner_radius=8,
                            text="Seçili Kaydı Sil",
                            command=self.del_selected_item, fg_color="#80BCBD", hover_color="#80BCBD").place(x=520, y=480)
        

        self.addSaleIconLabel.bind("<Button-1>", lambda event: self.newSaleEntry(event))
        self.addSaleIconLabel.bind("<Enter>", self.on_cursor_enter)
        self.addSaleIconLabel.bind("<Leave>", self.on_cursor_leave)

    def newSaleEntry(self, event):
        self.addSalePageFrame = customtkinter.CTkToplevel(self.master)
        self.addSalePageFrame.geometry("400x390") 
        self.addSalePageFrame.title("Satış Kayıt Ekleme") 
        self.addSalePageFrame.attributes("-topmost", True)
        self.addSalePageFrame.config(bg="white")
        customerArray =  []
        productsArray = []
        
        tupleCustomers = selectQuery("SELECT ad FROM musteriler")
        for customer in tupleCustomers:
            customerArray.append(customer[0])

        tupleProducts = selectQuery("SELECT urunadi FROM urunler")
        for product in tupleProducts:
            productsArray.append(product[0])

        customtkinter.CTkLabel(master=self.addSalePageFrame, text="Müşteri: ", font=("Helvetica", 20, "bold"), text_color="black").place(x=30, y=30)
        self.customerCombobox = customtkinter.CTkComboBox(master=self.addSalePageFrame,
                                            values=list(customerArray), width=200)
        self.customerCombobox.place(x=140, y=30)


        customtkinter.CTkLabel(master=self.addSalePageFrame, text="Ürün: ", font=("Helvetica", 20, "bold"), text_color="black").place(x=30, y=100)
        self.productCombobox = customtkinter.CTkComboBox(master=self.addSalePageFrame,
                                            values=list(productsArray), width=200)
        self.productCombobox.place(x=140, y=100)


        customtkinter.CTkLabel(master=self.addSalePageFrame, text="Fiyat: ", font=("Helvetica", 20, "bold"), text_color="black").place(x=30, y=170)
        self.priceEntry = customtkinter.CTkEntry(master=self.addSalePageFrame, placeholder_text="Fiyat")
        self.priceEntry.place(x=140, y=170)

        customtkinter.CTkButton(master=self.addSalePageFrame,
                            width=140,
                            height=45,
                            border_width=0,
                            corner_radius=8,
                            text="Satış Ekle",
                            command=self.addNewSaleBtn_Call, fg_color="#80BCBD", hover_color="#80BCBD").place(x=120, y=280)
        
    
    def addNewSaleBtn_Call(self):
        mixQuery("INSERT INTO satislar(urunid, musteriid, satistarihi, miktar, toplamfiyat)  VALUES ((SELECT urunid FROM urunler WHERE urunadi='"+str(self.productCombobox.get())+"'), (SELECT musteriid FROM musteriler WHERE ad='"+str(self.customerCombobox.get())+"'), CURRENT_TIMESTAMP,1,"+str(self.priceEntry.get())+")")
        self.addSalePageFrame.destroy()
        refreshSalesPage = salesPage(self.master)

    def del_selected_item(self):
        selectedIndex = self.salesListbox.curselection()
        if selectedIndex:
            selectedItem = self.salesListbox.get(selectedIndex)
            selectedItemId = re.search(r'^(\d+)-\)', selectedItem).group(1)
            mixQuery("DELETE FROM satislar WHERE satisid="+str(selectedItemId))
            refreshSalesPage = salesPage(self.master)


    def on_cursor_enter(self, event):
        # İmleç şeklini değiştir
        event.widget.config(cursor="hand2")

    def on_cursor_leave(self, event):
        # İmleç şeklini eski haline getir
        event.widget.config(cursor="")  


class productsPage(customtkinter.CTkFrame):
    def __init__(self, master):

        self.master = master
        self.master.title("Ürünler Ekranı")
        self.master.geometry("930x600")
 
        MenuBar(self.master)
        
        self.master.products_frame = customtkinter.CTkFrame(self.master, corner_radius=0, fg_color="transparent")
        self.master.products_frame.grid_columnconfigure(0, weight=1)
        self.master.products_frame.grid(row=0, column=1, sticky="nsew")

        products = selectQuery("SELECT urunid, urunadi, aciklama, fiyat, stokmiktari  FROM urunler;")

        label = customtkinter.CTkLabel(master=self.master.products_frame, text="Ürünler", font=("Helvetica", 24, "bold"),)
        label.place(x=50, y=60)

        self.addProductIcon = customtkinter.CTkImage(light_image=Image.open(os.path.join("images/icons", "add.png")), size=(45 , 45))
        self.addProductIconLabel = customtkinter.CTkLabel(master=self.master.products_frame, image=self.addProductIcon, text='')  
        self.addProductIconLabel.place(x=620, y=58)

        self.productsListbox = CTkListbox(self.master.products_frame, width=600, height=300, text_color="black")
        self.productsListbox.place(x=50, y=130)

        customtkinter.CTkButton(master=self.master.products_frame,
                            width=140,
                            height=45,
                            border_width=0,
                            corner_radius=8,
                            text="Seçili Kaydı Sil",
                            command=self.del_selected_item, fg_color="#80BCBD", hover_color="#80BCBD").place(x=520, y=480)
        
        customtkinter.CTkButton(master=self.master.products_frame,
                            width=140,
                            height=45,
                            border_width=0,
                            corner_radius=8,
                            text="Seçili Kaydı Düzenle",
                            command=self.productUpdatePage, fg_color="#80BCBD", hover_color="#80BCBD").place(x=80, y=480)

        for product in products:
            saleDataForListbox = str(product[0]) + "-)" + "Ürün: " + str(product[1]) + "  Açıklama: " + str(product[2]) + "  Stok: " + str(product[3]) + "   " + str(product[4])
            self.productsListbox.insert("END", saleDataForListbox)
        

        self.addProductIconLabel.bind("<Button-1>", lambda event: self.newSaleEntry(event))
        self.addProductIconLabel.bind("<Enter>", self.on_cursor_enter)
        self.addProductIconLabel.bind("<Leave>", self.on_cursor_leave)


    def del_selected_item(self):
        selectedIndex = self.productsListbox.curselection()
        if selectedIndex:
            selectedItem = self.productsListbox.get(selectedIndex)
            selectedItemId = re.search(r'^(\d+)-\)', selectedItem).group(1)
            mixQuery("DELETE FROM urunler WHERE urunid="+str(selectedItemId))
            refreshProductsPage = productsPage(self.master)


    def productUpdatePage(self):
        self.updateProductPageFrame = customtkinter.CTkToplevel(self.master)
        self.updateProductPageFrame.geometry("370x390") 
        self.updateProductPageFrame.title("Ürün Güncelleme") 
        self.updateProductPageFrame.attributes("-topmost", True)
        self.updateProductPageFrame.config(bg="white")
            
        selectedIndex = self.productsListbox.curselection()
        if selectedIndex:
            selectedItem = self.productsListbox.get(selectedIndex)
            self.selectedItemId = re.search(r'^(\d+)-\)', selectedItem).group(1)
            releatedProduct = selectQuery("SELECT urunadi, aciklama, fiyat, stokmiktari FROM urunler WHERE urunid="+str(self.selectedItemId))

            customtkinter.CTkLabel(master=self.updateProductPageFrame, text="Ürün: ", font=("Helvetica", 20, "bold"), text_color="black").place(x=30, y=30)
            self.productNameEntry = customtkinter.CTkEntry(master=self.updateProductPageFrame, placeholder_text="Ürün Adı")
            self.productNameEntry.place(x=175, y=30)
            self.productNameEntry.insert(0, releatedProduct[0][0])

            customtkinter.CTkLabel(master=self.updateProductPageFrame, text="Açıklama: ", font=("Helvetica", 20, "bold"), text_color="black").place(x=30, y=80)
            self.productDescpEntry = customtkinter.CTkEntry(master=self.updateProductPageFrame, placeholder_text="Açıklama")
            self.productDescpEntry.place(x=175, y=80)
            self.productDescpEntry.insert(0, releatedProduct[0][1])

            customtkinter.CTkLabel(master=self.updateProductPageFrame, text="Fiyat: ", font=("Helvetica", 20, "bold"), text_color="black").place(x=30, y=130)
            self.productPriceEntry = customtkinter.CTkEntry(master=self.updateProductPageFrame, placeholder_text="Fiyat")
            self.productPriceEntry.place(x=175, y=130)
            self.productPriceEntry.insert(0, releatedProduct[0][2])

            customtkinter.CTkLabel(master=self.updateProductPageFrame, text="Stok Miktarı: ", font=("Helvetica", 20, "bold"), text_color="black").place(x=30, y=180)
            self.productStockEntry = customtkinter.CTkEntry(master=self.updateProductPageFrame, placeholder_text="Stok")
            self.productStockEntry.place(x=175, y=180)
            self.productStockEntry.insert(0, releatedProduct[0][3])

            customtkinter.CTkButton(master=self.updateProductPageFrame,
                                width=140,
                                height=45,
                                border_width=0,
                                corner_radius=8,
                                text="Değişiklikleri Kaydet",
                                command=self.update_selected_item, fg_color="#80BCBD", hover_color="#80BCBD").place(x=100, y=270)

    def update_selected_item(self):
        mixQuery("UPDATE urunler SET urunadi='"+str(self.productNameEntry.get())+"', aciklama='"+str(self.productDescpEntry.get())+"', fiyat='"+str(self.productPriceEntry.get())+ "', stokmiktari='"+str(self.productStockEntry.get())+"' WHERE urunid="+str(self.selectedItemId))
        self.updateProductPageFrame.destroy()
        refreshProductsPage = productsPage(self.master)

        
    def on_cursor_enter(self, event):
        # İmleç şeklini değiştir
        event.widget.config(cursor="hand2")

    def on_cursor_leave(self, event):
        # İmleç şeklini eski haline getir
        event.widget.config(cursor="")  


class customersPage(customtkinter.CTkFrame):
    def __init__(self, master):

        self.master = master
        self.master.title("Müşteriler Ekranı")
        self.master.geometry("930x600")
 
        MenuBar(self.master)
        
        self.master.customers_frame = customtkinter.CTkFrame(self.master, corner_radius=0, fg_color="transparent")
        self.master.customers_frame.grid_columnconfigure(0, weight=1)
        self.master.customers_frame.grid(row=0, column=1, sticky="nsew")

        customers = selectQuery("select musteriid, ad, telefon, adres, eposta from musteriler;")

        label = customtkinter.CTkLabel(master=self.master.customers_frame, text="Ürünler", font=("Helvetica", 24, "bold"),)
        label.place(x=50, y=60)


        self.customersListbox = CTkListbox(self.master.customers_frame, width=600, height=300, text_color="black")
        self.customersListbox.place(x=50, y=130)

        customtkinter.CTkButton(master=self.master.customers_frame,
                            width=140,
                            height=45,
                            border_width=0,
                            corner_radius=8,
                            text="Seçili Kaydı Sil",
                            command=self.del_selected_item, fg_color="#80BCBD", hover_color="#80BCBD").place(x=520, y=480)
        
        for customer in customers:
            saleDataForListbox = str(customer[0]) + "-)" + "Ad: " + str(customer[1][:10]) + "...  Telefon: " + str(customer[2]) + "  Adres: " + str(customer[3][:5]) + "...   Eposta: " + str(customer[4])
            self.customersListbox.insert("END", saleDataForListbox)
        

    def del_selected_item(self):
        selectedIndex = self.customersListbox.curselection()
        if selectedIndex:
            selectedItem = self.customersListbox.get(selectedIndex)
            selectedItemId = re.search(r'^(\d+)-\)', selectedItem).group(1)
            mixQuery("DELETE FROM musteriler WHERE musteriid="+str(selectedItemId))
            refreshProductsPage = customersPage(self.master)



class totalPage(customtkinter.CTkFrame):
    def __init__(self, master):

        self.master = master
        self.master.title("Satış Raporu Ekranı")
        self.master.geometry("930x600")
 
        MenuBar(self.master)
        
        self.master.sales_frame = customtkinter.CTkFrame(self.master, corner_radius=0, fg_color="transparent")
        self.master.sales_frame.grid_columnconfigure(0, weight=1)
        self.master.sales_frame.grid(row=0, column=1, sticky="nsew")

        totalsales = selectQuery("SELECT musteriler.ad, SUM(toplamfiyat)  FROM satislar, musteriler  WHERE satislar.musteriid = musteriler.musteriid  GROUP BY musteriler.ad, satislar.musteriid  HAVING SUM(toplamfiyat) > 0;")

        label = customtkinter.CTkLabel(master=self.master.sales_frame, text="Toplam Satışlar", font=("Helvetica", 24, "bold"),)
        label.place(x=50, y=60)

        self.salesListbox = CTkListbox(self.master.sales_frame, width=600, height=300, text_color="black")
        self.salesListbox.place(x=50, y=130)

        for sale in totalsales:
            saleDataForListbox = str(sale[0]) + ": " + str(sale[1]) + "TL"
            self.salesListbox.insert("END", saleDataForListbox)
        


def mixQuery(query):
    try:

        cursor.execute(query)
        connection.commit()

    except Exception as error:
        print("Error while connecting to PostgreSQL:", error)


def selectQuery(query):
    try:

        cursor.execute(query)
        sales = cursor.fetchall()

        return sales


    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)



if __name__ == "__main__":  
    global connection, cursor
    host = ''
    dbname = ''
    user = ''
    password = ''
    port = ''  
    
        # Veritabanına bağlan
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    cursor = connection.cursor()
    
    root = customtkinter.CTk()
    customtkinter.set_appearance_mode("light")
    app = salesPage(root)
    root.mainloop()