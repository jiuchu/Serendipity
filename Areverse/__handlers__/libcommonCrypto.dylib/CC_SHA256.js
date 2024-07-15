{
  /**
   * Called synchronously when about to call CC_SHA256.
   *
   * @this {object} - Object allowing you to store state for use in onLeave.
   * @param {function} log - Call this function with a string to be presented to the user.
   * @param {array} args - Function arguments represented as an array of NativePointer objects.
   * For example use args[0].readUtf8String() if the first argument is a pointer to a C string encoded as UTF-8.
   * It is also possible to modify arguments by assigning a NativePointer object to an element of this array.
   * @param {object} state - Object allowing you to keep state across function calls.
   * Only one JavaScript function will execute at a time, so do not worry about race-conditions.
   * However, do not use this to store function arguments across onEnter/onLeave, but instead
   * use "this" which is an object for keeping state local to an invocation.
   */
  onEnter(log, args, state) {
    log('CC_SHA256() 函数被调用');

    // args[0] is the input data pointer
    // args[1] is the input data length
    // args[2] is the output hash pointer

    // Read input data
    var inputData = args[0].readByteArray(args[1].toInt32());
    log('入参数据: ' + hexdump(inputData, { offset: 0, length: args[1].toInt32(), header: false, ansi: false }));

    // Store output pointer for use in onLeave
    this.outputPtr = args[2];
  },

  /**
   * Called synchronously when about to return from CC_SHA256.
   *
   * See onEnter for details.
   *
   * @this {object} - Object allowing you to access state stored in onEnter.
   * @param {function} log - Call this function with a string to be presented to the user.
   * @param {NativePointer} retval - Return value represented as a NativePointer object.
   * @param {object} state - Object allowing you to keep state across function calls.
   */
  onLeave(log, retval, state) {
    // Read the resulting hash
    var outputHash = this.outputPtr.readByteArray(32); // SHA256 outputs 32 bytes
    log('返回值: ' + hexdump(outputHash, { offset: 0, length: 32, header: false, ansi: false }));
  }
}
