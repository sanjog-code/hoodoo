import struct, json

with open('public/models/tee_p5.glb', 'rb') as f:
    f.seek(12)
    chunk_len, chunk_type = struct.unpack('<II', f.read(8))
    gltf_json = json.loads(f.read(chunk_len))
    f.seek(12 + 8 + chunk_len)
    b_len, b_type = struct.unpack('<II', f.read(8))
    bin_data = f.read(b_len)

for mesh in gltf_json.get('meshes', []):
    for prim in mesh.get('primitives', []):
        pos_idx = prim['attributes']['POSITION']
        uv_idx = prim['attributes']['TEXCOORD_0']
        pos_acc = gltf_json['accessors'][pos_idx]
        uv_acc = gltf_json['accessors'][uv_idx]
        
        pos_bv = gltf_json['bufferViews'][pos_acc['bufferView']]
        uv_bv = gltf_json['bufferViews'][uv_acc['bufferView']]
        
        pos_offset = pos_bv.get('byteOffset', 0) + pos_acc.get('byteOffset', 0)
        uv_offset = uv_bv.get('byteOffset', 0) + uv_acc.get('byteOffset', 0)
        
        count = pos_acc['count']
        pos_verts = [struct.unpack_from('<3f', bin_data, pos_offset + i*12) for i in range(count)]
        uv_verts = [struct.unpack_from('<2f', bin_data, uv_offset + i*8) for i in range(count)]
        
        # Check vertices with Z > 0 (towards camera at +Z) vs Z < 0 (away from camera)
        z_pos_uvs = [uv_verts[i] for i in range(count) if pos_verts[i][2] > 0.05]
        z_neg_uvs = [uv_verts[i] for i in range(count) if pos_verts[i][2] < -0.05]
        
        print(f"Mesh: {mesh.get('name')}")
        if z_pos_uvs:
            u_pos = [u[0] for u in z_pos_uvs]
            print(f"   Vertices facing camera (+Z): U range [{min(u_pos):.2f}, {max(u_pos):.2f}], mean={sum(u_pos)/len(u_pos):.2f}")
        if z_neg_uvs:
            u_neg = [u[0] for u in z_neg_uvs]
            print(f"   Vertices facing back   (-Z): U range [{min(u_neg):.2f}, {max(u_neg):.2f}], mean={sum(u_neg)/len(u_neg):.2f}")
