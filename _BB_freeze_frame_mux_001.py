'''
Script Name: Mux Freeze Frame
Script Version: 1.0
Flame Version: 2021.1
Written by: Bryan Bayley
Creation Date: 08.12.21

Description: Add a mux after the selected node and freeze on this frame.
'''

def get_batch_custom_ui_actions():

    def get_context():
        import flame
        contexts = flame.batch.contexts
        first_context_slot = 1
        last_context_slot = 10

        for context in range(first_context_slot, last_context_slot + 1):
            if not contexts.has_key(context):
                return context
        return None

    def scope_node(selection):
        import flame
        for item in selection:
            if isinstance(item, flame.PyNode):
                return True
        return False

    def add_mux_and_freeze(selection):
        del selection
        import flame
        current = flame.batch.current_node.get_value()
        time = flame.batch.current_frame

        # Create the MUX node
        mux = flame.batch.create_node("Mux")
        mux.pos_x = current.pos_x + 200
        mux.pos_y = current.pos_y
        context_nb = get_context()
        if context_nb is not None:
            mux.set_context(context_nb, "Result")
        mux.range_active = True
        mux.range_start = time
        mux.range_end = time
        mux.before_range = "Repeat First"
        mux.after_range = "Repeat Last"

        # Connect the Result output socket to the MUX's Front socket
        flame.batch.connect_nodes(current, "Default", mux, "Default")

        # Connect the first Matte output socket to the MUX's Matte socket
        socket_number = 0
        for socket in current.output_sockets:
            if socket_number > 0:
                if "matte" in socket.lower() or "alpha" in socket.lower():
                    flame.batch.connect_nodes(current, socket, mux, "Matte_0")
                    break
            socket_number = socket_number + 1

    return [
        {
            "name": "Batch Nodes...",
            "actions": [
                {
                    "name": "Add Mux and Freeze",
                    "isVisible": scope_node,
                    "execute": add_mux_and_freeze
                }
            ]
        }
    ]
