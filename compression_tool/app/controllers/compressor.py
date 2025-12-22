import os
import json
import asyncio
import tempfile
from typing import Dict
from bitstring import  BitStream, Bits
from app.services.counter import Counter
from app.services.huffman_tree import HuffmanNodeGenerator


class Compressor:
    def __init__(self) -> None:
        self.generator = HuffmanNodeGenerator()
        self.prefix_table : Dict[bytes, str] = {}

    async def encode(self, file: str):
        if not os.path.exists(file):
            raise Exception("File is not exist")
            
        file_name = os.path.basename(file)

        counting_table = Counter.from_file(file)
        tree = self.generator.gen_node(counting_table)
        self.prefix_table = self.generator.gen_prefix_table(tree)
        with open("prefix_table.json", "w") as f:
            for key, value in self.prefix_table.items():
                f.write(f"{key}={value}\n")
        header = self._get_header_data(counting_table, file_name)
        
        # Tạo file tạm để lưu các chunk
        temp_dir = tempfile.mkdtemp()
        chunk_files = []
        chunk_index = 0
        current_chunk = BitStream()
        current_chunk.append(header)
        chunk_size_limit = 4 * 1024  # 4KB
        
        # Đọc và xử lý file theo chunks 4KB
        loop = asyncio.get_event_loop()
        
        # Đọc toàn bộ file thành các chunks
        def read_all_chunks():
            chunks = []
            with open(file, "rb") as f:
                while True:
                    chunk = f.read(4 * 1024)
                    if not chunk:
                        break
                    chunks.append(chunk)
            return chunks
        
        all_chunks = await loop.run_in_executor(None, read_all_chunks)
        
        # Xử lý từng chunk bất đồng bộ
        for chunk_data in all_chunks:
            # Xử lý chunk này
            encoded_chunk = await self._encode_chunk(chunk_data)
            current_chunk.append(encoded_chunk)
            
            # Nếu đã đủ 4KB, lưu vào file
            if len(current_chunk) >= chunk_size_limit * 8:  # bitstring tính theo bits
                chunk_file = os.path.join(temp_dir, f"chunk_{chunk_index}.bin")
                await loop.run_in_executor(None, self._write_chunk, chunk_file, current_chunk)
                chunk_files.append(chunk_file)
                chunk_index += 1
                current_chunk = BitStream()
        
        # Lưu phần còn lại nếu có
        if len(current_chunk) > 0:
            chunk_file = os.path.join(temp_dir, f"chunk_{chunk_index}.bin")
            await loop.run_in_executor(None, self._write_chunk, chunk_file, current_chunk)
            chunk_files.append(chunk_file)
        
        # Kết hợp tất cả các chunk vào file cuối cùng
        output_file = file + ".huffman"
        await self._combine_chunks(chunk_files, output_file, loop)
        
        # Xóa các file tạm
        for chunk_file in chunk_files:
            os.remove(chunk_file)
        os.rmdir(temp_dir)
    
    async def _encode_chunk(self, chunk_data: bytes) -> Bits:
        """Encode một chunk dữ liệu thành Huffman code."""
        loop = asyncio.get_event_loop()
        encoded_bits = await loop.run_in_executor(None, self._encode_chunk_sync, chunk_data)
        return encoded_bits
    
    def _encode_chunk_sync(self, chunk_data: bytes) -> Bits:
        """Encode chunk đồng bộ (chạy trong executor)."""
        encoded = BitStream()
        for byte_val in chunk_data:
            byte_key = bytes([byte_val])
            if byte_key in self.prefix_table:
                code_str = self.prefix_table[byte_key]
                encoded.append(Bits(bin=code_str))
        return encoded
    
    def _write_chunk(self, file_path: str, chunk: BitStream):
        """Ghi chunk vào file."""
        with open(file_path, "wb") as f:
            chunk.tofile(f)
    
    async def _combine_chunks(self, chunk_files: list, output_file: str, loop: asyncio.AbstractEventLoop):
        """Kết hợp tất cả các chunk vào file cuối cùng."""
        with open(output_file, "wb") as output:
            for chunk_file in chunk_files:
                chunk_data = await loop.run_in_executor(None, self._read_chunk_file, chunk_file)
                output.write(chunk_data)
    
    def _read_chunk_file(self, file_path: str) -> bytes:
        """Đọc chunk từ file."""
        with open(file_path, "rb") as f:
            return f.read()
    
    
    def _get_code_by_letter(self, key: str) -> str:
        """Get the Huffman code for a given letter."""
        return self.prefix_table.get(key, "")


    def _get_header_data(self, table_info: Dict[bytes, int], file_name: str) -> Bits:
        content = ""
        for key, value in table_info.items():
            content += f"{key}={value},"
        content = content[:-1]
        return Bits(f"vct@@{file_name}///{content}@@vct".encode("utf-8"))
