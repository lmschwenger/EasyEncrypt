# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 19:00:38 2023

@author: lasse
"""

m0 = "attack at dawn"
c0 = "09e1c5f70a65ac519458e7e53f36"
m1 = "attack at dusk"

m0_bytes = bytes(m0, "utf-8")  # convert m0 to bytes
m1_bytes = bytes(m1, "utf-8")  # convert m1 to bytes
c0_bytes = bytes.fromhex(c0)  # convert c0 to bytes

temp = bytes([m0_b ^ c0_b for m0_b, c0_b in zip(m0_bytes, c0_bytes)])  # compute XOR of m0_bytes and c0_bytes
c1_bytes = bytes([temp_b ^ m1_b for temp_b, m1_b in zip(temp, m1_bytes)])  # compute XOR of temp and m1_bytes

c1 = c1_bytes.hex()  # convert result back to hex string

print(c1)  # print the result