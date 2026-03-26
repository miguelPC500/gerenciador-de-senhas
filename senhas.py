import customtkinter as ctk
import json
import os
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Gerenciador(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("750x750")
        self.title("Gerenciador de Senhas")

        # Título
        ctk.CTkLabel(self, text="Gerenciador de Senhas", font=("Arial", 30, "bold")).pack(pady=20)

        
        self.frame_inputs = ctk.CTkFrame(self)
        self.frame_inputs.pack(pady=10, padx=20, fill="x")
        
        self.entry_nome = ctk.CTkEntry(self.frame_inputs, placeholder_text="Site/Serviço")
        self.entry_nome.grid(row=0, column=0, padx=10, pady=10)

        self.entry_senha = ctk.CTkEntry(self.frame_inputs, placeholder_text="Senha", show="*")
        self.entry_senha.grid(row=0, column=1, padx=10, pady=10)

        self.btn_add = ctk.CTkButton(self.frame_inputs, text="Adicionar", command=self.adicionar)
        self.btn_add.grid(row=0, column=2, padx=10, pady=10)

        # --- LISTA COM SCROLL ---
        self.lista_frame = ctk.CTkScrollableFrame(self, label_text="Senhas Salvas")
        self.lista_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.carregar()

    def carregar(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        if os.path.exists('gerenciar.json'):
            with open('gerenciar.json', 'r') as f:
                try:
                    dados = json.load(f)
                    for i, item in enumerate(dados):
                        
                        ctk.CTkLabel(self.lista_frame, text=item['nome'], width=150, anchor="w").grid(row=i, column=0, padx=10)
                        
                        
                        ent = ctk.CTkEntry(self.lista_frame, width=150, show="*")
                        ent.insert(0, item['senha'])
                        ent.configure(state="readonly")
                        ent.grid(row=i, column=1, padx=10, pady=5)

                        # Botão Ver
                        btn_v = ctk.CTkButton(self.lista_frame, text="Ver", width=50, fg_color="gray")
                        btn_v.configure(command=lambda e=ent, b=btn_v: self.toggle(e, b))
                        btn_v.grid(row=i, column=2, padx=5)

                        # Botão Excluir
                        btn_d = ctk.CTkButton(self.lista_frame, text="X", width=30, fg_color="red", hover_color="darkred")
                        btn_d.configure(command=lambda n=item['nome']: self.deletar(n))
                        btn_d.grid(row=i, column=3, padx=10)
                except: pass

    def toggle(self, entry, btn):
        if entry.cget("show") == "*":
            entry.configure(show="")
            btn.configure(text="Ocultar")
        else:
            entry.configure(show="*")
            btn.configure(text="Ver")

    def adicionar(self):
        n, s = self.entry_nome.get(), self.entry_senha.get()
        if n and s:
            subprocess.run(["node", "gerenciar.js", "add", n, s])
            self.entry_nome.delete(0, 'end')
            self.entry_senha.delete(0, 'end')
            self.carregar()

    def deletar(self, nome):
        subprocess.run(["node", "gerenciar.js", "delete", nome])
        self.carregar()

if __name__ == "__main__":
    Gerenciador().mainloop()